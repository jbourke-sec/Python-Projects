from datetime import datetime
import json
import os
import zipfile
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulnProject.settings')
django.setup()
from django.db import models
from vulnApp.models import asset, vulnerability
import urllib.request
from vulnApp.formulas import formulas
from cpe.cpe2_3 import CPE2_3
from celery import Celery


app = Celery('tasks', broker='pyamqp://guest@localhost//')

class CveEntry():
    def __init__(self, cve_item):
        self.cve_dict = dict()
        for key, value in cve_item.items():
            self.cve_dict[key] = value
        self.cve_dict['accessVector'] = None
        self.cve_dict['confidentialityImpact'] = None
        self.cve_dict['availabilityImpact'] = None
        self.cve_dict['userInteraction'] = None
        self.cve_dict['privilegesRequired'] = None
        self.cve_dict['scope'] = None
        self.cve_dict['integrityImpact'] = None
        self.cve_dict['rc'] = None
        self.cve_dict['rl'] = None
        self.cve_dict['ecm'] = None
        self.cve_dict['attackComplexity'] = None
        self.cve_dict['cpeUri'] = 'None'
        
        self.cve_dict['ID'] = cve_item['cve']['CVE_data_meta']['ID']
        
        self.cve_dict['publishedDate'] = cve_item['publishedDate']
        datetime_object = datetime.strptime(self.cve_dict['publishedDate'], '%Y-%m-%dT%H:%MZ')
        self.cve_dict['publishedDate'] = datetime_object
        
        self.cve_dict['lastModifiedDate'] = self.cve_dict['lastModifiedDate']
        datetime_object = datetime.strptime(self.cve_dict['lastModifiedDate'], '%Y-%m-%dT%H:%MZ')
        self.cve_dict['lastModifiedDate'] = datetime_object
        
        self.cve_dict['newestDate'] = min([self.cve_dict['publishedDate'], self.cve_dict['lastModifiedDate']])
        descriptions = list()
        for description_data in cve_item['cve']['description']['description_data']:
            descriptions.append(description_data['value'])
        self.cve_dict['descriptions'] = descriptions
        
        self.description = 'no_description_info'
        if len(descriptions) > 0:
            self.description = '|'.join(descriptions)
        try:
            cpe_list_length=len(cve_item['configurations']['nodes'])
            cpe_list = list()
            affectAssets = asset.objects.none()
            if (cpe_list_length !=0):
                for i in range(0,cpe_list_length):
                    if 'children' in cve_item['configurations']['nodes'][i]:
                        cpe_child_list_length=len(cve_item['configurations']['nodes'][i]['children'])
                        if (cpe_child_list_length !=0):
                            for j in range(0,cpe_child_list_length):
                                if('cpe_match' in cve_item['configurations']['nodes'][i]['children'][j]):
                                    cpes = cve_item['configurations']['nodes'][i]['children'][j]['cpe_match']
                                    for cpe in cpes:
                                        if 'cpe23Uri' in cpe:
                                            if str(cpe['vulnerable']) == 'True':
                                                cpe_list.append(str(cpe['cpe23Uri']))
                        else:
                            if('cpe_match' in cve_item['configurations']['nodes'][i]):
                                cpes = cve_item['configurations']['nodes'][i]['cpe_match']
                                for cpe in cpes:
                                    if 'cpe23Uri' in cpe:
                                        if cpe['vulnerable'] == 'True':
                                                cpe_list.append(cpe['cpe23Uri'])
                            else:
                                cpe_inner_list_length=len(cve_item['configurations']['nodes'])
                                if (cpe_inner_list_length!=0):
                                    for k in range(0,cpe_inner_list_length):
                                        if('cpe_match' in cve_item['configurations']['nodes'][i]):
                                            cpes = cve_item['configurations']['nodes'][i]['cpe_match']
                                            for cpe in cpes:
                                                #vulnTech = CPESet2_3()
                                                if 'cpe23Uri' in cpe:
                                                    if cpe['vulnerable'] == 'True':
                                                        cpe_list.append(cpe['cpe23Uri'])
                        if len(cpe_list) != 0:
                            self.cve_dict['cpeUri'] = " ".join(cpe_list)
                            assets = asset.objects.all()
                            for x in assets:
                                #try:
                                if str(x.tags) != '' and isinstance(x.tags, str): 
                                    wfns = x.tags.split(",")
                                   # print(wfns)
                                    if len(wfns) > 0:
                                        cpeSet=list()
                                        for y in range(0, len(wfns)):
                                            try:
                                                uri = CPE2_3(wfns[y])
                                                cpeSet.append([uri.get_vendor(), uri.get_product()])
                                            except Exception as e:
                                                print(e)
                                    for y in range(0, len(cpe_list)):
                                        tagUri = CPE2_3(cpe_list[y])
                                        if [tagUri.get_vendor(), tagUri.get_product()] in cpeSet:
                                            if(list(affectAssets) == list(asset.objects.none())):
                                                affectAssets = asset.objects.filter(assetid=x.assetid)
                                            else:
                                                found = asset.objects.filter(assetid=x.assetid)
                                                affectAssets = affectAssets.union(found)   
                        else:
                           self.cve_dict['cpeUri'] = "None"
        except Exception as e:
            print(str(e), 'at ',['configurations'])
        # scoring
        self.cvss2_score = 0
        self.cvss3_score = 0
        self.scoring = 'no_score_info'
        cvss_scores = list()
        for key in ['baseMetricV2', 'baseMetricV3']:
            if key in self.cve_dict['impact']:
                cvss_scores.append('{}:{}'.format( \
                    key[-2:], \
                    self.cve_dict['impact'][key]['impactScore']))
                    
                try:
                    if key == 'baseMetricV2':
                        self.cvss2_score = float(self.cve_dict['impact'][key]['impactScore'])
                        if cve_item['impact'][key]['cvssV2']['accessVector'] == 'NETWORK':
                            self.cve_dict['accessVector'] = 'Network'
                        elif cve_item['impact'][key]['cvssV2']['accessVector'] == 'LOCAL':
                            self.cve_dict['accessVector'] = 'Local'
                        elif cve_item['impact'][key]['cvssV2']['accessVector'] == 'PHYSICAL':
                            self.cve_dict['accessVector'] = 'Physical'
                        elif cve_item['impact'][key]['cvssV2']['accessVector'] == 'ADJACENT_NETWORK':
                            self.cve_dict['accessVector'] = 'Adjacent Network'
                        else:
                           self.cve_dict['accessVector'] = 'Local' 
                        if cve_item['impact'][key]['cvssV2']['accessComplexity'] == 'HIGH':
                            self.cve_dict['attackComplexity'] = 'High'
                        elif cve_item['impact'][key]['cvssV2']['accessComplexity'] == 'LOW':
                            self.cve_dict['attackComplexity'] = 'Low'
                        else:
                            self.cve_dict['attackComplexity'] = 'Not Defined'
                        if cve_item['impact'][key]['obtainUserPrivilege'] == 'true':
                            self.cve_dict['privilegesRequired'] = 'High'
                        elif cve_item['impact'][key]['obtainUserPrivilege'] == 'false':
                            self.cve_dict['privilegesRequired'] = 'Low'
                        else:
                            self.cve_dict['privilegesRequired'] = 'None'
                        if cve_item['impact'][key]['userInteractionRequired'] == 'true':
                            self.cve_dict['userInteraction'] = 'Required'
                        elif cve_item['impact'][key]['userInteractionRequired'] == 'false':
                            self.cve_dict['userInteraction'] = 'None'
                        else:
                            self.cve_dict['userInteraction'] = 'Not Defined'
                        if cve_item['impact'][key]['cvssV2']['confidentialityImpact'] == 'COMPLETE':
                            self.cve_dict['confidentialityImpact'] = 'High'
                        elif cve_item['impact'][key]['cvssV2']['confidentialityImpact'] == 'PARTIAL':
                            self.cve_dict['confidentialityImpact'] = 'Low'
                        else:
                          self.cve_dict['confidentialityImpact'] = 'None'
                        if cve_item['impact'][key]['cvssV2']['integrityImpact'] == 'COMPLETE':
                            self.cve_dict['integrityImpact'] = 'High'
                        elif cve_item['impact'][key]['cvssV2']['integrityImpact'] == 'PARTIAL':
                            self.cve_dict['integrityImpact'] = 'Low'
                        else:
                          self.cve_dict['integrityImpact'] = 'None' 
                        if cve_item['impact'][key]['cvssV2']['availabilityImpact'] == 'COMPLETE':
                            self.cve_dict['availabilityImpact'] = 'High'
                        elif cve_item['impact'][key]['cvssV2']['availabilityImpact'] == 'PARTIAL':
                            self.cve_dict['availabilityImpact'] = 'Low'
                        else:
                          self.cve_dict['availabilityImpact'] = 'None'
                        self.cve_dict['scope'] = 'Unchanged'

                    elif key == 'baseMetricV3':
                        self.cvss3_score = float(self.cve_dict['impact'][key]['impactScore'])
                        if cve_item['impact'][key]['cvssV3']['attackVector'] == 'NETWORK':
                            self.cve_dict['accessVector'] = 'Network'
                        elif cve_item['impact'][key]['cvssV3']['attackVector'] == 'LOCAL':
                            self.cve_dict['accessVector'] = 'Local'
                        elif cve_item['impact'][key]['cvssV3']['attackVector'] == 'PHYSICAL':
                            self.cve_dict['accessVector'] = 'Physical'
                        elif cve_item['impact'][key]['cvssV3']['attackVector'] == 'ADJACENT_NETWORK':
                            self.cve_dict['accessVector'] = 'Adjacent Network'
                        else:
                            self.cve_dict['accessVector'] = 'Local'
                        if cve_item['impact'][key]['cvssV3']['attackComplexity'] == 'HIGH':
                            self.cve_dict['attackComplexity'] = 'High'
                        elif cve_item['impact'][key]['cvssV3']['attackComplexity'] == 'LOW':
                            self.cve_dict['attackComplexity'] = 'Low'
                        else:
                            self.cve_dict['attackComplexity'] = 'Not Defined'
                        if cve_item['impact'][key]['cvssV3']['privilegesRequired'] == 'HIGH':
                            self.cve_dict['privilegesRequired'] = 'High'
                        elif cve_item['impact'][key]['cvssV3']['privilegesRequired'] == 'LOW':
                            self.cve_dict['privilegesRequired'] = 'Low'
                        else:
                            self.cve_dict['privilegesRequired'] = 'None'
                        if cve_item['impact'][key]['cvssV3']['userInteraction'] == 'REQUIRED':
                            self.cve_dict['userInteraction'] = 'Required'
                        elif cve_item['impact'][key]['cvssV3']['userInteraction'] == 'NONE':
                            self.cve_dict['userInteraction'] = 'None'
                        else:
                            self.cve_dict['userInteraction'] = 'Not Defined'
                        if cve_item['impact'][key]['cvssV3']['confidentialityImpact'] == 'HIGH':
                            self.cve_dict['confidentialityImpact'] = 'High'
                        elif cve_item['impact'][key]['cvssV3']['confidentialityImpact'] == 'LOW':
                            self.cve_dict['confidentialityImpact'] = 'Low'
                        else:
                          self.cve_dict['confidentialityImpact'] = 'None'
                        if cve_item['impact'][key]['cvssV3']['integrityImpact'] == 'HIGH':
                            self.cve_dict['integrityImpact'] = 'High'
                        elif cve_item['impact'][key]['cvssV3']['integrityImpact'] == 'LOW':
                            self.cve_dict['integrityImpact'] = 'Low'
                        else:
                          self.cve_dict['integrityImpact'] = 'None' 
                        if cve_item['impact'][key]['cvssV3']['availabilityImpact'] == 'HIGH':
                            self.cve_dict['availabilityImpact'] = 'High'
                        elif cve_item['impact'][key]['cvssV3']['availabilityImpact'] == 'LOW':
                            self.cve_dict['availabilityImpact'] = 'Low'
                        else:
                          self.cve_dict['availabilityImpact'] = 'None'
                        if cve_item['impact'][key]['cvssV3']['scope'] == 'UNCHANGED':
                            self.cve_dict['scope'] = 'Unchanged'
                        else:
                            self.cve_dict['scope'] = 'Changed'
                   
                        
                except:
                    pass
                self.cve_dict['ecm'] = 'Not Defined'
                self.cve_dict['rc'] = 'Not Defined'
                self.cve_dict['rl'] = 'Not Defined'
                
                iscbase = formulas.iscbase(self.cve_dict['confidentialityImpact'], self.cve_dict['integrityImpact'], self.cve_dict['availabilityImpact'])
                impactscore = formulas.impactScore(iscbase, self.cve_dict['scope'])
                exploit = formulas.exploitScore(self.cve_dict['accessVector'],self.cve_dict['attackComplexity'], self.cve_dict['privilegesRequired'], self.cve_dict['userInteraction'], self.cve_dict['scope'])
                base = formulas.baseScore(iscbase, self.cve_dict['scope'], impactscore, exploit)
                if base >= 9:
                    risksc = 'Critical'
                elif base >= 7:
                    risksc = 'High'
                elif base >= 4:
                    risksc = 'Medium'
                else:
                    risksc = 'Low'
                vuln, created = vulnerability.objects.update_or_create(cve=self.cve_dict['ID'],
                defaults= dict(cpe=self.cve_dict['cpeUri'], risk=risksc, mav=self.cve_dict['accessVector'], mac=self.cve_dict['attackComplexity'], mui=self.cve_dict['userInteraction'], mpr=self.cve_dict['privilegesRequired'], ms=self.cve_dict['scope'], mc=self.cve_dict['confidentialityImpact'], mi=self.cve_dict['integrityImpact'], ma=self.cve_dict['availabilityImpact'], rc=self.cve_dict['rc'], rl=self.cve_dict['rl'], ecm=self.cve_dict['ecm'], description=self.cve_dict['descriptions'], dayZero=self.cve_dict['publishedDate']
                ))
                vuln1 = vulnerability.objects.get(cve=self.cve_dict['ID'])
                print(affectAssets)
                affectAssets = affectAssets.union(vuln1.assetid.all())
                vuln1.assetid.set(affectAssets)
                vuln1.save()
        if len(cvss_scores) > 0:
            self.scoring = '|'.join(cvss_scores)
        
    def __str__(self):
        return '{}: {}, {}, {}'.format( \
            self.cve_dict['ID'], \
            self.scoring, \
            self.cve_dict['newestDate'], \
            self.cve_dict['impact'], \
            self.description[:50])

    def parseCVEfiles(path_to_json_file):
        if not os.path.isfile(path_to_json_file):
            print('File {} does not exist!'.format(path_to_json_file))
            return None
            
        with open(path_to_json_file, encoding="utf8") as json_file:
            print('Parsing file {}'.format(path_to_json_file))
            cve_data = json.load(json_file)
            CveEntry_list = [CveEntry(cve_dict) for cve_dict in cve_data['CVE_Items']]
            CveEntry_list.sort(key=lambda x: x.cve_dict['newestDate'], reverse=True)
            CveEntry_list.sort(key=lambda x: x.cvss2_score, reverse=True)
            CveEntry_list.sort(key=lambda x: x.cvss3_score, reverse=True)
                
            
            
    def extractZIP(directory=os.getcwd()):
        if not os.path.isdir(directory):
            print('Directory {} does not exist!'.format(directory))
            return list()
        
        zip_file_count = 0
        zip_extracted = list()
        zip_failed = list()
        extracted_filenames = list()
        for my_file in os.listdir(directory):
            if my_file.lower().endswith('.zip'):
                path_to_zip_file = os.path.join(directory, my_file)
                zip_file_count += 1
                print('Extracting ZIP file {}: {}'.format(zip_file_count, path_to_zip_file))
                try:
                    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                        zip_ref.extractall()
                        for member in zip_ref.infolist():
                            extracted_filenames.append(os.path.join(directory, member.filename))
                            print('Member filename: {}'.format(member.filename))
                    zip_extracted.append(path_to_zip_file)
                except Exception as e:
                    print('FAILED to extract ZIP file: {}'.format(path_to_zip_file))
                    print(e)
                    zip_failed.append(path_to_zip_file)

        print('{} ZIP files processed in total:'.format(zip_file_count))
        for i, zip_file in enumerate(zip_extracted, 1):
            print('\t{}) {} SUCCESS'.format(i, zip_file))
        for i, zip_file in enumerate(zip_failed, 1):
            print('\t{}) {} FAILED'.format(i, zip_file))
        return extracted_filenames

    def downloadCVEfiles(directory=os.getcwd()):
        zip_json_modified = 'nvdcve-1.1-modified.json.zip'
        zip_json_modified_url = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-modified.json.zip'
        zip_json_recent = 'nvdcve-1.1-recent.json.zip'
        zip_json_recent_url = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip'
        
        downloaded_files = list()
        for url in [zip_json_modified_url, zip_json_recent_url]:
            local_filename = os.path.join(directory, url.split('/')[-1])
            
            if os.path.isfile(local_filename):
                dt_now = datetime.now()
                dt_modified = datetime.fromtimestamp(os.path.getmtime(local_filename))
                print('Last modified: {}'.format(dt_modified))
                dt_created = datetime.fromtimestamp(os.path.getctime(local_filename))
                print('Created: {}'.format(dt_created))
                print('Age of file {}: {}'.format(local_filename, (dt_now - dt_created).total_seconds()))
                if ((dt_now - dt_created).total_seconds() > 60*60):
                    print('Older than 1 hour! Downloading new file...')
                    my_file = CveEntry.download_remote_file(url, local_filename)
                    if my_file is not None:
                        downloaded_files.append(my_file)
            else:
                CveEntry.download_remote_file(url, local_filename)
                my_file = CveEntry.download_remote_file(url, local_filename)
                if my_file is not None:
                    downloaded_files.append(my_file)
                    
        return downloaded_files

    def download_remote_file(url, local_filename):
        if not '/' in url:
            print('No URL provided!')
            return None
        try:
            urllib.request.urlretrieve(url, local_filename)
            return local_filename
        except Exception as e:
            print('FAILED to download URL: {}'.format(url))
            print(e)      
        return None
    @app.task
    def main():
        zip_files = CveEntry.downloadCVEfiles()
        print('{} files downloaded'.format(len(zip_files)))
        for i, zip_file in enumerate(zip_files, 1):
            print('\t{}) {}'.format(i, zip_file))
        json_files = CveEntry.extractZIP()
        print(', '.join(json_files))
        for json_file in json_files:
            CveEntry.parseCVEfiles(json_file)
