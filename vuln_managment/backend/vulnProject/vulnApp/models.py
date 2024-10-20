from datetime import timedelta, datetime
import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from datetime import datetime, timedelta

from datetime import datetime
import json
import os
import zipfile
import urllib.request
from .formulas import formulas
from cpe.cpe2_3 import CPE2_3
class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
        
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        print(self.pk)
        return token.decode('utf-8')

class policy(models.Model):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    NOTDEFINED='Not Defined'
    REQ = [
       (HIGH, ('High Requirement')),
       (MEDIUM, ('Medium Requirement')),
       (LOW, ('Low Requirement')),
       (NOTDEFINED, ('Not Defined')),
   ]
   
    policyid = models.AutoField(primary_key=True, unique=True,auto_created=True)
    cpe=models.CharField(max_length=100, null=True, blank=True)
    confidentialityreq=models.CharField(choices=REQ, default=NOTDEFINED,max_length=20)
    integrityreq=models.CharField(choices=REQ, default=NOTDEFINED, max_length=20)
    availabilityreq=models.CharField(choices=REQ, default=NOTDEFINED, max_length=20)
    category=models.CharField(max_length=100, null=True, blank=True, unique=True)
    def __str__(self):
        return self.category

class playbook(models.Model):
    playbookid = models.AutoField(primary_key=True, unique=True,auto_created=True)
    category = models.CharField(max_length=30, default='Default')
    patchacquirement = models.CharField(max_length=30,default= "Patch Acquirement")
    patchvalidation = models.CharField(max_length=30, default = 'Patch Validation')
    verification = models.CharField(max_length=30, default='Patch Verification')
    rollout = models.CharField(max_length=30, default='Patch Rollout')
    notes = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.category
    
class asset(models.Model):
    assetid = models.AutoField(primary_key=True, unique=True,auto_created=True)
    cpe = models.CharField(max_length=20)
    risk=models.CharField(max_length=20)
    baseSLA = models.IntegerField(null=True, blank=True)
    policyid=ForeignKey(policy, models.SET_NULL, null=True)
    category = models.CharField(max_length=30)
    hostname = models.CharField(max_length=100, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.cpe
    def appendTag(self, tag):
        self.tags+=', '
        self.tags+=tag
        return self
    def removeTag(self, tag):
        taglist = self.tags.split(', ')
        taglist.remove(tag)
        self.tag = taglist
        return self.tag

class vulnerability(models.Model):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'
    NONE='None'
    NOTDEFINED='Not Defined'
    NETWORK = 'Network'
    ADJNETWORK = 'Adjacent Network'
    LOCAL = 'Local'
    PHYSICAL='Physical'
    CHANGED='Changed'
    UNCHANGED='Unchanged'
    REQUIRED='Required'
    UNPROVEN = 'Unproven that exploit exists'
    PROOFOFCON = 'Proof of concept code'
    FUNCTIONALEXP = 'Functional exploit exists'
    OFFICIALFIX = 'Official fix'
    TEMPFIX = 'Temporary fix'
    WORKAROUND='Workaround'
    UNAVAILABLE='Unavailable'
    CONFIRMED = 'Confirmed'
    REASONABLE='Reasonable'
    UNKNOWN='Unknown'

    SCOPE = [
       (CHANGED, ('High Requirement')),
       (UNCHANGED, ('Medium Requirement')),
       (NOTDEFINED, ('Not Defined')),
   ]
    MUI = [
       (REQUIRED, ('Required')),
       (NONE, ('None')),
       (NOTDEFINED, ('Not Defined')),
   ]
    MAC = [
       (HIGH, ('High Requirement')),
       (LOW, ('Low Requirement')),
       (NOTDEFINED, ('Not Defined')),
   ]
    MAV = [
       (NETWORK, ('Network')),
       (ADJNETWORK, ('Adjacent Network')),
       (LOCAL, ('Local')),
       (PHYSICAL, ('Physical')),
   ]
   
    MPR = [
       (HIGH, ('High Requirement')),
       (LOW, ('Low Requirement')),
       (NONE, ('None')),
       (NOTDEFINED, ('Not Defined')),
   ]
    ECM = [
       (HIGH,('High')),
       (FUNCTIONALEXP,('Functional exploit exists')),
       (PROOFOFCON,('Proof of concept code')),
       (UNPROVEN,('Unproven that exploit exists')),
       (NOTDEFINED,('Not Defined')),
    ]
    RL = [
        (UNAVAILABLE,('Unavailable')),
        (WORKAROUND,('Workaround')),
        (TEMPFIX,('Temporary fix')),
        (OFFICIALFIX,('Official fix')),
        (NOTDEFINED,('Not Defined')),
    ]
    RC = [
        (UNKNOWN, ('Unknown')),
        (REASONABLE,('Reasonable')),
        (CONFIRMED,('Confirmed')),
        (NOTDEFINED,('Not Defined')),
    ]
    CI = [
       (HIGH, ('High')),
       (LOW, ('Low')),
       (NONE, ('None')),
   ]
    vulnid = models.AutoField(primary_key=True, unique=True, auto_created=True)
    #assetid = ForeignKey(asset, models.SET_NULL, null=True)
    assetid = ManyToManyField(asset, blank = True)
    threat = models.TextField(null=True, blank=True)
    cve = models.CharField(max_length=150, unique=True)
    cpe = models.TextField(null=True, blank=True)
    risk = models.CharField(max_length=20)
    baseSLA = models.TimeField(null=True, blank=True)
    cwe = models.CharField(max_length=20, null=True, blank=True)
    mav=models.CharField(choices=MAV, default=NETWORK, max_length=20)
    mac=models.CharField(choices=MAC, default=NOTDEFINED, max_length=20)
    mpr=models.CharField(choices=MPR,default=NOTDEFINED, max_length=20)
    mui=models.CharField(choices=MUI, default=NOTDEFINED, max_length=20)
    ms=models.CharField(choices=SCOPE,default=NOTDEFINED, max_length=20)
    mc=models.CharField(choices=MPR, default=NOTDEFINED, max_length=20)
    mi=models.CharField(choices=MPR, default=NOTDEFINED, max_length=20)
    ma=models.CharField(choices=MPR, default=NOTDEFINED, max_length=20)
    rc=models.CharField(choices=RC, default=NOTDEFINED, max_length=20)
    rl=models.CharField(choices=RL, default=NOTDEFINED, max_length=20)
    ecm=models.CharField(choices=ECM, default=NOTDEFINED, max_length=30)
    description = models.TextField(null=True, blank=True)
    dayZero = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.cpe
class ticket(models.Model):
#progress will require pulling choice field from policy
    ticketNumber = models.AutoField(primary_key=True, unique=True, auto_created=True)
    summary = models.TextField(null=True, blank=True)
    validatedsummary = models.TextField(null=True, blank=True)
    verifiedsummary = models.TextField(null=True, blank=True)
    rolledsummary = models.TextField(null=True, blank=True)
    progress = models.CharField(max_length=20, blank=True)
    assignedTo = models.CharField(max_length=200, default="unassigned", blank=True)
    group = models.CharField(max_length=40, null=True, blank=True)
    timeStarted = models.DateTimeField(blank=True, editable=True, null=True)
    timePatchAquired = models.DateTimeField(blank=True, editable=True, null=True)
    timeValidated = models.DateTimeField(blank=True, editable=True, null=True)
    timeVerified = models.DateTimeField(blank=True, editable=True, null=True)
    timeRolledout = models.DateTimeField(blank=True, editable=True, null=True)
    timeClosed = models.DateTimeField(blank=True, editable=True, null=True)
    cve = models.CharField(max_length=15)
    vulnid=ForeignKey(vulnerability,null=True, blank=True, on_delete=models.SET_NULL)
    cvss = models.DecimalField(decimal_places=2, max_digits=4)
    qa = models.TextField(null=True, blank=True)
    sla = models.DateTimeField(null=True, blank=True)
    exposure = models.TextField(null=True, blank=True)
    threat = models.TextField(null=True, blank=True)
    assets= models.ManyToManyField(asset, blank=True)
    outcome=models.CharField(null=True, blank=True, max_length=20)
    playbookid=ForeignKey(playbook, models.SET_NULL, null=True, blank=True)
    acquired = models.BooleanField(default=False)
    validated = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    rolledout = models.BooleanField(default=False)
    enscore = models.CharField(null=True, blank=True, max_length=20)
    iscbase = models.CharField(null=True, blank=True, max_length=20)
    temporal = models.CharField(null=True, blank=True, max_length=20)
    exploitScore = models.CharField(null=True, blank=True, max_length=20)
    iscmodified = models.CharField(null=True, blank=True, max_length=20)
    impactModScore = models.CharField(null=True, blank=True, max_length=20)
    impactScore = models.CharField(null=True, blank=True, max_length=20)
    environmentalScore = models.CharField(null=True, blank=True, max_length=20)
    def __str__(self):
        return self.cve    
class scan(models.Model):
    scanid = models.AutoField(primary_key=True, unique=True, auto_created=True)
    scanScope = models.CharField(max_length=100)
    timeToStart = models.DateTimeField()
    userId = models.IntegerField()#pk for Users need to set this
    def __str__(self):
        return self.scanid

class scanResult(models.Model):
    resultId = models.AutoField(primary_key=True, unique=True, auto_created=True)
    scanid = ForeignKey(scan, models.CASCADE)
    assetid = ForeignKey(asset, models.CASCADE)
    cve = models.CharField(max_length=15)
    def __str__(self):
        return self.resultId
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
    def main():
        zip_files = CveEntry.downloadCVEfiles()
        print('{} files downloaded'.format(len(zip_files)))
        for i, zip_file in enumerate(zip_files, 1):
            print('\t{}) {}'.format(i, zip_file))
        json_files = CveEntry.extractZIP()
        print(', '.join(json_files))
        for json_file in json_files:
            CveEntry.parseCVEfiles(json_file)





