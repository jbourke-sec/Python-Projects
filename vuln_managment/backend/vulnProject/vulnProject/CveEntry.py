import os
#import re
import requests
import json
import zipfile
from collections import OrderedDict, Counter
from datetime import datetime, timedelta
import os
import time
import urllib.request
import pprint

#from models import vulnerability
pp = pprint.PrettyPrinter(indent=4)


class CveEntry():
    def __init__(self, cve_item):
        # copy all key-value pairs into new dict
        self.cve_dict = dict()
        for key, value in cve_item.items():
            self.cve_dict[key] = value
        
        self.cve_dict['ID'] = cve_item['cve']['CVE_data_meta']['ID']
        
        self.cve_dict['publishedDate'] = cve_item['publishedDate']
        datetime_object = datetime.strptime(self.cve_dict['publishedDate'], '%Y-%m-%dT%H:%MZ') # '2019-03-26T18:29Z'
        self.cve_dict['publishedDate'] = datetime_object
        #print(cve_dict['publishedDate'])
        
        self.cve_dict['lastModifiedDate'] = self.cve_dict['lastModifiedDate']
        datetime_object = datetime.strptime(self.cve_dict['lastModifiedDate'], '%Y-%m-%dT%H:%MZ') # '2019-04-03T17:22Z'
        self.cve_dict['lastModifiedDate'] = datetime_object
        #print(cve_dict['lastModifiedDate'])
        #self.cve_dict['publishedDate'] = cve_item['publishedDate']
        
        self.cve_dict['newestDate'] = min([self.cve_dict['publishedDate'], self.cve_dict['lastModifiedDate']])
        
        # description
        descriptions = list()
        for description_data in cve_item['cve']['description']['description_data']:
            descriptions.append(description_data['value'])
        self.cve_dict['descriptions'] = descriptions
        
        self.description = 'no_description_info'
        if len(descriptions) > 0:
            self.description = '|'.join(descriptions)
        
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
                        if cve_item['impact'][key]['cvssV2']['accessComplexity'] == 'HIGH':
                            self.cve_dict['attackComplexity'] = 'High'
                        elif cve_item['impact'][key]['cvssV2']['accessComplexity'] == 'LOW':
                            self.cve_dict['attackComplexity'] = 'Low'
                        else:
                            self.cve_dict['attackComplexity'] = 'Not Defined'
                        if cve_item['impact']['obtainUserPrivilege'] == 'true':
                            self.cve_dict['privilegesRequired'] = 'High'
                        elif cve_item['impact']['obtainUserPrivilege'] == 'false':
                            self.cve_dict['privilegesRequired'] = 'Low'
                        else:
                            self.cve_dict['privilegesRequired'] = 'None'
                        if cve_item['impact']['userInteractionRequired'] == 'true':
                            self.cve_dict['userInteraction'] = 'Required'
                        elif cve_item['impact']['userInteractionRequired'] == 'false':
                            self.cve_dict['userInteraction'] = 'None'
                        else:
                            self.cve_dict['userInteraction'] = 'Not Defined'
                        if cve_item['impact'][key]['confidentialityImpact'] == 'COMPLETE':
                            self.cve_dict['confidentialityImpact'] = 'High'
                        elif cve_item['impact'][key]['confidentialityImpact'] == 'PARTIAL':
                            self.cve_dict['confidentialityImpact'] = 'Low'
                        else:
                          self.cve_dict['confidentialityImpact'] = 'None'
                        if cve_item['impact'][key]['integrityImpact'] == 'COMPLETE':
                            self.cve_dict['integrityImpact'] = 'High'
                        elif cve_item['impact'][key]['integrityImpact'] == 'PARTIAL':
                            self.cve_dict['integrityImpact'] = 'Low'
                        else:
                          self.cve_dict['integrityImpact'] = 'None' 
                        if cve_item['impact'][key]['availabilityImpact'] == 'COMPLETE':
                            self.cve_dict['availabilityImpact'] = 'High'
                        elif cve_item['impact'][key]['availabilityImpact'] == 'PARTIAL':
                            self.cve_dict['availabilityImpact'] = 'Low'
                        else:
                          self.cve_dict['availabilityImpact'] = 'None'
                        self.cve_dict['scope'] = 'Unchanged'

                    elif key == 'baseMetricV3':
                        self.cvss3_score = float(self.cve_dict['impact'][key]['impactScore'])
                        if cve_item['impact'][key]['attackeVector'] == 'NETWORK':
                            self.cve_dict['accessVector'] = 'Network'
                        elif cve_item['impact'][key]['attackVector'] == 'LOCAL':
                            self.cve_dict['accessVector'] = 'Local'
                        elif cve_item['impact'][key]['attackVector'] == 'PHYSICAL':
                            self.cve_dict['accessVector'] = 'Physical'
                        elif cve_item['impact'][key]['attackVector'] == 'ADJACENT_NETWORK':
                            self.cve_dict['accessVector'] = 'Adjacent Network'
                        if cve_item['impact'][key]['attackComplexity'] == 'HIGH':
                            self.cve_dict['attackComplexity'] = 'High'
                        elif cve_item['impact'][key]['attackComplexity'] == 'LOW':
                            self.cve_dict['attackComplexity'] = 'Low'
                        else:
                            self.cve_dict['attackComplexity'] = 'Not Defined'
                        if cve_item['impact'][key]['privilegesRequired'] == 'HIGH':
                            self.cve_dict['privilegesRequired'] = 'High'
                        elif cve_item['impact'][key]['privilegesRequired'] == 'LOW':
                            self.cve_dict['privilegesRequired'] = 'Low'
                        else:
                            self.cve_dict['privilegesRequired'] = 'None'
                        if cve_item['impact'][key]['userInteraction'] == 'REQUIRED':
                            self.cve_dict['userInteraction'] = 'Required'
                        elif cve_item['impact'][key]['userInteraction'] == 'NONE':
                            self.cve_dict['userInteraction'] = 'None'
                        else:
                            self.cve_dict['userInteraction'] = 'Not Defined'
                        if cve_item['impact'][key]['confidentialityImpact'] == 'HIGH':
                            self.cve_dict['confidentialityImpact'] = 'High'
                        elif cve_item['impact'][key]['confidentialityImpact'] == 'LOW':
                            self.cve_dict['confidentialityImpact'] = 'Low'
                        else:
                          self.cve_dict['confidentialityImpact'] = 'None'
                        if cve_item['impact'][key]['integrityImpact'] == 'HIGH':
                            self.cve_dict['integrityImpact'] = 'High'
                        elif cve_item['impact'][key]['integrityImpact'] == 'LOW':
                            self.cve_dict['integrityImpact'] = 'Low'
                        else:
                          self.cve_dict['integrityImpact'] = 'None' 
                        if cve_item['impact'][key]['availabilityImpact'] == 'HIGH':
                            self.cve_dict['availabilityImpact'] = 'High'
                        elif cve_item['impact'][key]['availabilityImpact'] == 'LOW':
                            self.cve_dict['availabilityImpact'] = 'Low'
                        else:
                          self.cve_dict['availabilityImpact'] = 'None'
                        if cve_item['impact'][key]['scope'] == 'UNCHANGED':
                            self.cve_dict['scope'] = 'Unchanged'
                        else:
                            self.cve_dict['scope'] = 'Changed'
                   
                        
                except:
                    pass
                self.cve_dict['ecm'] = 'Not Defined'
                self.cve_dict['rc'] = 'Not Defined'
                self.cve_dict['rl'] = 'Not Defined'
                #vuln, created = vulnerability.objects.update_or_create(cve=self.cve_dict['ID'], cpe='Undefined', risk='Undefined', mav=self.cve_dict['accessVector'], mac=self.cve_dict['attackComplexity'], mui=self.cve_dict['userInteraction'], mpr=self.cve_dict['privilegesRequired'], ms=self.cve_dict['scope'], mc=self.cve_dict['confidentialityImpact'], mi=self.cve_dict['integrityImpact'], ma=self.cve_dict['availabilityImpact'], rc=self.cve_dict['rc'], rl=self.cve_dict['rl'], ecm=self.cve_dict['ecm'])
        if len(cvss_scores) > 0:
            self.scoring = '|'.join(cvss_scores)
        
    def __str__(self):
        return '{}: {}, {}, {}'.format( \
            self.cve_dict['ID'], \
            self.scoring, \
            self.cve_dict['newestDate'], \
            self.cve_dict['impact'], \
            self.description[:50])

def parse_NVD_CVE_files(path_to_json_file):
    if not os.path.isfile(path_to_json_file):
        print('File {} does not exist!'.format(path_to_json_file))
        return None
        
    with open(path_to_json_file, encoding="utf8") as json_file:
        print('Parsing file {}'.format(path_to_json_file))
        cve_data = json.load(json_file)
        #pp.pprint(cve_data)
        print('Number of CVE entries: {}'.format(len(cve_data['CVE_Items'])))
        print('-----')
        pp.pprint(cve_data['CVE_Items'][0].keys())
        print('-----')
        pp.pprint(cve_data['CVE_Items'][1].keys())
        
        # query certain values from the dictionary
        #cve_data['CVE_Items'][1].keys = dict.fromkeys(['cve', 'configurations', 'impact', 'publishedDate', 'lastModifiedDate'])
        CveEntry_list = [CveEntry(cve_dict) for cve_dict in cve_data['CVE_Items']]
            
        print('Number of CVE entries in cve_dict_list: {}'.format(len(CveEntry_list)))
        # sort CVE entries by newest date
        CveEntry_list.sort(key=lambda x: x.cve_dict['newestDate'], reverse=True)
        for cve_entry in CveEntry_list[0:20]:
            print(cve_entry)
           
        print('\nSorted by CVSS 2 score:')
        # sort CVE entries by CVSS 2 score
        CveEntry_list.sort(key=lambda x: x.cvss2_score, reverse=True)
        for cve_entry in CveEntry_list[0:20]:
            print(cve_entry)
        
        print('\nSorted by CVSS 3 score:')
        # sort CVE entries by CVSS 3 score
        CveEntry_list.sort(key=lambda x: x.cvss3_score, reverse=True)
        for cve_entry in CveEntry_list[0:20]:
            print(cve_entry)
            
        
        
def extract_ZIP_files(directory=os.getcwd()):
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
    
    # print statistics
    print('{} ZIP files processed in total:'.format(zip_file_count))
    for i, zip_file in enumerate(zip_extracted, 1):
        print('\t{}) {} SUCCESS'.format(i, zip_file))
    for i, zip_file in enumerate(zip_failed, 1):
        print('\t{}) {} FAILED'.format(i, zip_file))
    return extracted_filenames

def download_NVD_CVE_files(directory=os.getcwd()):
    zip_json_modified = 'nvdcve-1.1-modified.json.zip'
    zip_json_modified_url = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-modified.json.zip'
    zip_json_recent = 'nvdcve-1.1-recent.json.zip'
    zip_json_recent_url = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip'
    
    downloaded_files = list()
    for url in [zip_json_modified_url, zip_json_recent_url]:
        local_filename = os.path.join(directory, url.split('/')[-1])
        
        if os.path.isfile(local_filename):
            # check age of file
            dt_now = datetime.now()
            dt_modified = datetime.fromtimestamp(os.path.getmtime(local_filename))
            print('Last modified: {}'.format(dt_modified))
            dt_created = datetime.fromtimestamp(os.path.getctime(local_filename))
            print('Created: {}'.format(dt_created))
            print('Age of file {}: {}'.format(local_filename, (dt_now - dt_created).total_seconds()))
            if ((dt_now - dt_created).total_seconds() > 60*60):
                print('Older than 1 hour! Downloading new file...')
                my_file = download_remote_file(url, local_filename)
                if my_file is not None:
                    downloaded_files.append(my_file)
        else:
            download_remote_file(url, local_filename)
            my_file = download_remote_file(url, local_filename)
            if my_file is not None:
                downloaded_files.append(my_file)
                
    return downloaded_files

def download_remote_file(url, local_filename):
    if not '/' in url:
        print('No URL provided!')
        return None
    
    # try to download the file
    try:
        urllib.request.urlretrieve(url, local_filename)
        return local_filename
    except Exception as e:
        print('FAILED to download URL: {}'.format(url))
        print(e)
    
    return None

def main():
    zip_files = download_NVD_CVE_files()
    print('{} files downloaded'.format(len(zip_files)))
    for i, zip_file in enumerate(zip_files, 1):
        print('\t{}) {}'.format(i, zip_file))
    json_files = extract_ZIP_files()
    print(', '.join(json_files))
    for json_file in json_files:
        parse_NVD_CVE_files(json_file)

if __name__ == '__main__':
    print(__package__)
    main()