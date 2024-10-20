from datetime import time, timedelta, datetime
import os
from django.http.response import JsonResponse
from .models import User, asset, playbook, policy, ticket, vulnerability
from .serializers import AssetSerializer, LoginSerializer, PlaybookSerializer, PolicySerializer, TicketSerializer, UserSerializer, VulnerabilitySerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .renderers import UserJSONRenderer
from rest_framework.generics import RetrieveUpdateAPIView
from .formulas import formulas
from django.db.models import F
from cpe.cpe2_3 import CPE2_3
import json
import os
import zipfile
import urllib.request
from .formulas import formulas
from cpe.cpe2_3 import CPE2_3

@api_view(['GET', 'POST'])
def queue(request):
    #CveEntry.main()
    if request.method == 'GET':
        tickets = ticket.objects.filter(assignedTo='unassigned').order_by('-cvss', 'timeStarted').exclude(progress='Closed')
        tickets_serializer = TicketSerializer(tickets, many=True)
        return JsonResponse(tickets_serializer.data, safe=False)
    elif request.method == 'POST':
        ticket_data = JSONParser().parse(request)
        ticket_serializer = TicketSerializer(data=ticket_data)
        vuln = vulnerability.objects.get(cve=ticket_serializer.initial_data['cve'])
        play = ticket_serializer.initial_data['playbookid']
        ticket_serializer.initial_data['vulnid.vulnid'] = vuln
        sla = vulnerability.objects.filter(cve=ticket_serializer.initial_data['cve']).values_list('assetid', flat=True).values_list('baseSLA', flat=True)
        sla = list(filter(None, sla))
        intlist = list()
        for x in sla:
           intlist.append(int((x.hour * 60 + x.minute) * 60 + x.second))
        intlist.append(ticket_serializer.initial_data['sla'])
        ticket_serializer.initial_data['sla'] = (datetime.now() + timedelta(seconds=min(intlist))).strftime("%Y-%m-%dT%H:%M:%SZ")
        if ticket_serializer.is_valid():
            play = playbook.objects.get(playbookid=play['playbookid'])
            vuln = vulnerability.objects.get(cve=ticket_serializer.validated_data['cve'])
            ticket_serializer.validated_data['vulnid'] = vuln
            ticket_serializer.validated_data['playbookid'] = play
            ticket_serializer.validated_data['progress'] = 'New'
            ticket_serializer.validated_data['assignedTo'] = 'unassigned'
            ticket_serializer.validated_data['group'] =  play.patchacquirement
            ticket_serializer.validated_data['timeClosed'] = None
            ticket_serializer.validated_data['timeStarted'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            ticket_serializer.validated_data['assets'] = vuln.assetid.all()
            ticket_serializer.validated_data['iscbase'] = formulas.iscbase(vuln.mc, vuln.ma, vuln.mi)
            ticket_serializer.validated_data['impactScore'] = formulas.impactScore(formulas.iscbase(vuln.mc, vuln.ma, vuln.mi), vuln.ms)
            ticket_serializer.validated_data['exploitScore'] = formulas.exploitScore(vuln.mav,vuln.mac, vuln.mpr, vuln.mui, vuln.ms)
            ticket_serializer.validated_data['cvss'] = formulas.baseScore(formulas.iscbase(vuln.mc, vuln.ma, vuln.mi), vuln.ms, formulas.impactScore(formulas.iscbase(vuln.mc, vuln.ma, vuln.mi), vuln.ms), formulas.exploitScore(vuln.mav,vuln.mac, vuln.mpr, vuln.mui, vuln.ms))
            ticket_serializer.validated_data['temporal'] = formulas.temporal(formulas.baseScore(formulas.iscbase(vuln.mc, vuln.ma, vuln.mi), vuln.ms, formulas.impactScore(formulas.iscbase(vuln.mc, vuln.ma, vuln.mi), vuln.ms), formulas.exploitScore(vuln.mav,vuln.mac, vuln.mpr, vuln.mui, vuln.ms)), vuln.ecm, vuln.rl, vuln.rc)
            assets3 = asset.objects.filter(assetid__in={instance.assetid for instance in vuln.assetid.all()}).filter(policyid__isnull = False)
            tempEnScore = 0
            tempIsc = 0
            if assets3.count() > 0:
                for instance in assets3:
                    currentPolicy = policy.objects.get(policyid = instance.policyid.policyid)
                    print(formulas.iscmodified(vuln.mc, vuln.mi, vuln.ma, currentPolicy.confidentialityreq, currentPolicy.integrityreq, currentPolicy.availabilityreq))
                    if formulas.iscmodified(vuln.mc, vuln.mi, vuln.ma, currentPolicy.confidentialityreq, currentPolicy.integrityreq, currentPolicy.availabilityreq) > tempIsc:
                        tempIsc = formulas.iscmodified(vuln.mc, vuln.mi, vuln.ma, currentPolicy.confidentialityreq, currentPolicy.integrityreq, currentPolicy.availabilityreq)
                        tempEnScore = formulas.environmentalScore(tempIsc, vuln.ms, formulas.impactModScore(tempIsc, vuln.ms), ticket_serializer.validated_data['exploitScore'], vuln.ecm, vuln.rl, vuln.rc)
                ticket_serializer.validated_data['environmentalScore'] = tempEnScore
                ticket_serializer.validated_data['iscmodified'] = tempIsc
            else:
                ticket_serializer.validated_data['environmentalScore'] = ticket_serializer.validated_data['cvss']
                ticket_serializer.validated_data['iscmodified'] = ticket_serializer.validated_data['iscbase']
            ticket_serializer.save()
            print(JsonResponse(ticket_serializer.data, status=status.HTTP_201_CREATED))
            return JsonResponse(ticket_serializer.data, status=status.HTTP_201_CREATED)
        print(ticket_serializer.errors) 
        return JsonResponse(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def getMyTickets(request):
    if request.method == 'GET':
        tickets = ticket.objects.filter(assignedTo = request.user.username).exclude(progress='Closed')   
        tickets_serializer = TicketSerializer(tickets, many=True)
    return JsonResponse(tickets_serializer.data, safe=False, status=status.HTTP_200_OK)
@api_view(['GET'])
def getClosedTickets(request):
    if request.method == 'GET':
        tickets = ticket.objects.filter(progress = "closed")
        tickets_serializer = TicketSerializer(tickets, many=True)
        return JsonResponse(tickets_serializer.data, safe=False, status=status.HTTP_200_OK)
def getGroupTickets(request, string):
    if request.method == 'GET':
        tickets = ticket.objects.filter(group = string).filter(assignedTo='unassigned')
        tickets_serializer = TicketSerializer(tickets, many=True)
        return JsonResponse(tickets_serializer.data, safe=False, status=status.HTTP_200_OK)
@api_view(['GET', 'PUT', 'DELETE'])
def viewTicket(request, ticketnumber):
    try:
        myticket = ticket.objects.get(ticketNumber=ticketnumber)
        if request.method == 'GET': 
            ticket_serializer = TicketSerializer(myticket) 
            return JsonResponse(ticket_serializer.data)
        elif request.method == 'PUT': 
            ticket_data = JSONParser().parse(request) 
            ticket_serializer = TicketSerializer(myticket, data=ticket_data)
            assets1=ticket_serializer.initial_data['assets']
            assets3 = asset.objects.filter(assetid__in={instance['assetid'] for instance in assets1}) 
            vuln = vulnerability.objects.get(cve=ticket_serializer.initial_data['cve'])
            assets2=vuln.assetid.all()
            if ticket_serializer.is_valid():

                assets3 = assets3.union(assets2)
                print(assets3)
                ticket_serializer.save()
                if(myticket.progress == 'New'):
                    myticket.progress = 'In Progress'
                if(myticket.acquired == True and myticket.timePatchAquired == None):
                    myticket.timePatchAquired = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                elif(myticket.validated == True and myticket.timeValidated == None):
                    myticket.timeValidated = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                elif(myticket.verified == True and myticket.timeVerified == None):
                    myticket.timeVerified = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                elif(myticket.rolledout == True and myticket.timeRolledout == None):
                    myticket.timeRolledout = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                if(myticket.progress == 'Closed' and myticket.timeClosed == None):
                    myticket.timeClosed = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                if(list(assets2) != list(assets3)):
                    assets3 = assets3.union(assets2)
                    myticket.assets.set(assets3)
                    sla = assets3.values_list('baseSLA', flat=True)
                    intlist = list()
                    for x in sla:
                        intlist.append(timedelta(seconds=x) + myticket.timeStarted)
                    intlist.append(myticket.sla)
                    print(intlist)
                    intlist = filter(None, intlist)
                    myticket.sla = min(intlist).strftime("%Y-%m-%dT%H:%M:%SZ")
                print(myticket.assets)
                myticket.save()
                return JsonResponse(ticket_serializer.data) 
            return JsonResponse(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            ticket.delete() 
            return JsonResponse({'message': 'Ticket was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except ticket.DoesNotExist:
        return JsonResponse({'message': 'Ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def assetList(request):
    if request.method == 'GET': 
        assets = asset.objects.all()
        asset_serializer = AssetSerializer(assets, many=True)
        return JsonResponse(asset_serializer.data, safe=False)
    elif request.method == 'POST':
        asset_data = JSONParser().parse(request)
        asset_serializer = AssetSerializer(data=asset_data)
        if asset_serializer.is_valid():
            asset_serializer.save()
            myAsset = asset.objects.get(assetid=asset_serializer['assetid'].value)
            cpelist = myAsset.tags.split(',')
            vulns = vulnerability.objects.all().exclude(cpe='None')
            if len(cpelist) > 0:
                for x in vulns:
                    cpeSet = list()
                    try:
                        urilist = x.cpe.split(' ')
                        for uri in urilist:
                            uri = CPE2_3(uri)
                            cpeSet.append([uri.get_vendor(), uri.get_product()])
                    except Exception as e:
                        print(e)  
                    for cpe in cpelist:
                        try:
                            tagUri = CPE2_3(cpe)
                            if [tagUri.get_vendor(), tagUri.get_product()] in cpeSet and myAsset not in x.assetid.values():
                                x.assetid.add(myAsset)
                                x.save()
                        except:
                            pass
            if(policy.objects.filter(category=myAsset.category).count() > 0):
                newPolicy = policy.objects.get(category=myAsset.category)
                myAsset.update(policyid=newPolicy)
            return JsonResponse(asset_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(asset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def assetListNoPolicy(request):
    if request.method == 'GET': 
        assets = asset.objects.filter(policyid=None)
        asset_serializer = AssetSerializer(assets, many=True)
        return JsonResponse(asset_serializer.data, safe=False)
@api_view(['GET', 'PUT', 'DELETE'])
def viewAsset(request, assetId):
    try:
        myAsset = asset.objects.get(assetid=assetId)
        if request.method == 'GET': 
            asset_serializer = AssetSerializer(myAsset) 
            return JsonResponse(asset_serializer.data)
        elif request.method == 'PUT': 
            asset_data = JSONParser().parse(request) 
            asset_serializer = AssetSerializer(myAsset, data=asset_data) 
            if asset_serializer.is_valid():
                asset_serializer.save()
                myAsset = asset.objects.get(assetid=assetId)
                cpelist = myAsset.tags.split(',')
                vulns = vulnerability.objects.all().exclude(cpe='None')
                if len(cpelist) > 0:
                    for x in vulns:
                        cpeSet = list()
                        try:
                            urilist = x.cpe.split(' ')
                            for uri in urilist:
                                uri = CPE2_3(uri)
                                cpeSet.append([uri.get_vendor(), uri.get_product()])
                        except Exception as e:
                            print(e)  
                        for cpe in cpelist:
                            try:
                                tagUri = CPE2_3(cpe)
                                if [tagUri.get_vendor(), tagUri.get_product()] in cpeSet and myAsset not in x.assetid.values():
                                    x.assetid.add(myAsset)
                                    x.save()
                            except:
                                pass
            myAsset = asset.objects.get(assetid=assetId)
            if(policy.objects.filter(category=myAsset.category).count() > 0):
                newPolicy = policy.objects.get(category=myAsset.category)
                myAsset.update(policyid=newPolicy)
                return JsonResponse(asset_serializer.data) 
            return JsonResponse(asset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE': 
            asset.delete() 
            return JsonResponse({'message': 'Asset was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except asset.DoesNotExist:
        return JsonResponse({'message': 'Asset does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
def vulnList(request):
    if request.method == 'GET': 
        vulns = vulnerability.objects.all()
        vuln_serializer = VulnerabilitySerializer(vulns, many=True)
        return JsonResponse(vuln_serializer.data, safe=False)
    elif request.method == 'POST':
        vuln_data = JSONParser().parse(request)
        vuln_serializer = VulnerabilitySerializer(data=vuln_data)
        if vuln_serializer.is_valid():
            vuln_serializer.save()
            myVuln = vulnerability.objects.get(vulnid=vuln_serializer['vulnid'].value)
            cpelist = myVuln.cpe.split(' ')
            assets = asset.objects.all().exclude(cpe__isnull=True)
            if len(cpelist) > 0:
                for x in assets:
                    cpeSet = list()
                    try:
                        urilist = x.cpe.split(',')
                        for uri in urilist:
                            uri = CPE2_3(uri)
                            cpeSet.append([uri.get_vendor(), uri.get_product()])
                    except Exception as e:
                        print(e)  
                    for cpe in cpelist:
                        try:
                            tagUri = CPE2_3(cpe)
                            if [tagUri.get_vendor(), tagUri.get_product()] in cpeSet and x not in myVuln.assetid.values():
                                myVuln.assetid.add(x)
                                myVuln.save()
                        except:
                            pass 
            return JsonResponse(vuln_serializer.data, status=status.HTTP_201_CREATED)
        print(vuln_serializer.errors)
        return JsonResponse(vuln_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def unremediatedVuln(request):
    if request.method == 'GET': 
        tickets = ticket.objects.all().values_list('cve')
        vulns = vulnerability.objects.all().exclude(cve__in = tickets).exclude(cpe='None')
        vuln_serializer = VulnerabilitySerializer(vulns, many=True)
        return JsonResponse(vuln_serializer.data, safe=False)
@api_view(['GET'])
def inProgressVuln(request):
    if request.method == 'GET': 
        tickets = ticket.objects.all().exclude(progress="closed").values_list('cve')
        vulns = vulnerability.objects.all().filter(cve__in = tickets)
        vuln_serializer = VulnerabilitySerializer(vulns, many=True)
        return JsonResponse(vuln_serializer.data, safe=False)
@api_view(['GET'])
def closedVuln(request):
    if request.method == 'GET': 
        tickets = ticket.objects.all().values_list('cve').filter(progress="closed")
        print(tickets)
        vulns = vulnerability.objects.all().filter(cve__in = tickets)
        vuln_serializer = VulnerabilitySerializer(vulns, many=True)
        return JsonResponse(vuln_serializer.data, safe=False)
@api_view(['GET'])
def vulnAffectAssets(request):
        if request.method == 'GET': 
            tickets = ticket.objects.all().values_list('cve')
            print(tickets)
            vulns = vulnerability.objects.all().exclude(assetid__isnull=True).exclude(cve__in = tickets)
            vuln_serializer = VulnerabilitySerializer(vulns, many=True)
            return JsonResponse(vuln_serializer.data, safe=False)
def vulnlast7days(request):
        if request.method == 'GET': 
            tickets = ticket.objects.all().exclude(progress="closed").values_list('cve')
            print(tickets)
            vulns = vulnerability.objects.filter(dayZero__gte=datetime.now()-timedelta(days=7)).exclude(cve__in = tickets)
            vuln_serializer = VulnerabilitySerializer(vulns, many=True)
            return JsonResponse(vuln_serializer.data, safe=False)
@api_view(['GET', 'PUT', 'DELETE'])
def viewVuln(request, vulnId):
    try:
        myVuln = vulnerability.objects.get(vulnid=vulnId)
        if request.method == 'GET': 
            vuln_serializer = VulnerabilitySerializer(myVuln) 
            return JsonResponse(vuln_serializer.data)
        elif request.method == 'PUT': 
            vuln_data = JSONParser().parse(request) 
            vuln_serializer = VulnerabilitySerializer(myVuln, data=vuln_data) 
            if vuln_serializer.is_valid(): 
                vuln_serializer.save()
                cpelist = myVuln.cpe.split(' ')
                assets = asset.objects.all().exclude(cpe__isnull=True)
                if len(cpelist) > 0:
                    for x in assets:
                        cpeSet = list()
                        try:
                            urilist = x.cpe.split(',')
                            for uri in urilist:
                                uri = CPE2_3(uri)
                                cpeSet.append([uri.get_vendor(), uri.get_product()])
                        except Exception as e:
                            print(e)  
                        for cpe in cpelist:
                            try:
                                tagUri = CPE2_3(cpe)
                                if [tagUri.get_vendor(), tagUri.get_product()] in cpeSet and x not in myVuln.assetid.values():
                                    myVuln.assetid.add(x)
                                    myVuln.save()
                            except:
                                pass
                return JsonResponse(vuln_serializer.data)
            print(vuln_serializer.errors)
            return JsonResponse(vuln_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            vulnerability.delete() 
            return JsonResponse({'message': 'Vulnerability was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except vulnerability.DoesNotExist:
        return JsonResponse({'message': 'Vulnerability does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
def playList(request):
    if request.method == 'GET': 
        plays = playbook.objects.all()
        play_serializer = PlaybookSerializer(plays, many=True)
        return JsonResponse(play_serializer.data, safe=False)
    elif request.method == 'POST':
        play_data = JSONParser().parse(request)
        play_serializer  = PlaybookSerializer(data=play_data)
        if play_serializer.is_valid():
            play_serializer.save()
            return JsonResponse(play_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(play_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def viewPlay(request, playbookId):
    try:
        play = playbook.objects.get(playbookid=playbookId)
        if request.method == 'GET': 
            play_serializer = PlaybookSerializer(play) 
            return JsonResponse(play_serializer.data)
        elif request.method == 'PUT': 
            play_data = JSONParser().parse(request) 
            play_serializer = PlaybookSerializer(play, data=play_data) 
            if play_serializer.is_valid(): 
                play_serializer.save() 
                return JsonResponse(play_serializer.data) 
            return JsonResponse(play_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            playbook.delete() 
            return JsonResponse({'message': 'Playbook was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except playbook.DoesNotExist:
        return JsonResponse({'message': 'Playbook does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
def policyList(request):
    if request.method == 'GET': 
        policies = policy.objects.all()
        policy_serializer = PolicySerializer(policies, many=True)
        return JsonResponse(policy_serializer.data, safe=False)
    elif request.method == 'POST':
        policy_data = JSONParser().parse(request)
        policy_serializer  = PolicySerializer(data=policy_data)
        if policy_serializer.is_valid():
            policy_serializer.save()
            mypolicy = policy.objects.get(policyid=policy_serializer['policyid'].value)
            assets = asset.objects.filter(category=mypolicy.category)
            if(asset.objects.filter(category=mypolicy.category).count() > 0):
                assets.update(policyid=mypolicy)
            return JsonResponse(policy_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(policy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def viewPolicy(request, policyId):
    try:
        Policy = policy.objects.get(policyid=policyId)
        if request.method == 'GET': 
            policy_serializer = PolicySerializer(Policy) 
            return JsonResponse(policy_serializer.data)
        elif request.method == 'PUT': 
            policy_data = JSONParser().parse(request) 
            policy_serializer = PolicySerializer(Policy, data=policy_data) 
            if policy_serializer.is_valid(): 
                policy_serializer.save()
                assets = asset.objects.filter(category=Policy.category)
                if(asset.objects.filter(category=Policy.category).count() > 0):
                    assets.update(policyid=Policy)
                return JsonResponse(policy_serializer.data) 
            return JsonResponse(policy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            policy.delete() 
            return JsonResponse({'message': 'Policy was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except policy.DoesNotExist:
        return JsonResponse({'message': 'Policy does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def returnClosedResults(request, days):
    if request.method == 'GET': 
        timedays = int(days)
        timedays = timedelta(days=timedays)
        timedays=datetime.now() - timedays
        response = list()
        result = dict()
        result['name'] = 'Accepted Risk'
        result['value'] = ticket.objects.filter(outcome='Accepted Risk', timeClosed__gte=timedays).count()
        response.append(result)
        result = dict()
        result['name'] = 'Remediated'
        result['value'] = ticket.objects.filter(outcome='Remediated', timeClosed__gte=timedays).count()
        response.append(result)
        result = dict()
        result['name'] = 'Mitigated'
        result['value'] = ticket.objects.filter(outcome='Mitigated', timeClosed__gte=timedays).count()
        response.append(result)
        return JsonResponse(response, safe=False)
@api_view(['GET'])
def affectVulnBySev(request):
    if request.method == 'GET': 
        response = list()
        result = dict()
        result['name'] = 'Critical'
        result['value'] = vulnerability.objects.filter(risk='Critical').exclude(assetid__isnull=True).count()
        response.append(result)
        result = dict()
        result['name'] = 'High'
        result['value'] = vulnerability.objects.filter(risk='High').exclude(assetid__isnull=True).count()
        response.append(result)
        result = dict()
        result['name'] = 'Medium'
        result['value'] = vulnerability.objects.filter(risk='Medium').exclude(assetid__isnull=True).count()
        response.append(result)
        result = dict()
        result['name'] = 'Low'
        result['value'] = vulnerability.objects.filter(risk='Low').exclude(assetid__isnull=True).count()
        response.append(result)
        return JsonResponse(response, safe=False)
@api_view(['GET'])
def metSLA(request, days):
    if request.method == 'GET': 
        timedays = int(days)
        timedays = timedelta(days=timedays)
        timedays=datetime.now() - timedays
        response = list()
        result = dict()
        result['name'] = 'Met SLA'
        result['value'] = ticket.objects.filter(sla__gte = F('timeClosed')).filter(timeClosed__gte=timedays).count()
        response.append(result)
        result = dict()
        result['name'] = 'Not Met SLA'
        result['value'] = ticket.objects.all().exclude(sla__gte = F('timeClosed')).filter(timeClosed__gte=timedays).exclude(sla__isnull=True).count()
        response.append(result)
        return JsonResponse(response, safe=False)
@api_view(['GET'])
def averageRemediationTimes(request, days):
    if request.method == 'GET': 
        timedays = int(days)
        timedays = timedelta(days=timedays)
        timedays=datetime.now() - timedays
        response = list()
        cve = 0
        sta = 1
        acq = 2
        val = 3
        ver = 4
        rol = 5
        hourinday = 24
        secinhour = 3600
        patchAcqList = list()
        patchValList = list()
        patchVerList = list()
        patchRolList = list()
        ticketStats = ticket.objects.filter(progress="closed", timeClosed__gte=timedays).values_list('cve', 'timeStarted', 'timePatchAquired', 'timeValidated', 'timeVerified', 'timeRolledout').exclude(outcome='Accepted Risk')
        print(ticketStats)
        for x in ticketStats:
            if any(y is None for y in x) == False:
                result = dict()
                result['name'] = x[cve]
                result['series'] = list()
                point = dict()
                point['name'] = 'Patch Acquired'
                point['value'] = ((x[acq] - x[sta]).days*hourinday) + ((x[acq] - x[sta]).seconds/secinhour)
                result['series'].append(point)
                patchAcqList.append(point['value'])
                point = dict()
                point['name'] = 'Patch Validated'
                point['value'] = ((x[val] - x[sta]).days*hourinday) + ((x[val] - x[sta]).seconds/secinhour)
                result['series'].append(point)
                patchValList.append(point['value'])
                point = dict()
                point['name'] = 'Patch Verified'
                point['value'] = ((x[ver] - x[sta]).days*hourinday) + ((x[ver] - x[sta]).seconds/secinhour)
                result['series'].append(point)
                patchVerList.append(point['value'])
                point = dict()
                point['name'] = 'Patch Rolled Out'
                point['value'] = ((x[rol] - x[sta]).days*hourinday) + ((x[rol] - x[sta]).seconds/secinhour)
                result['series'].append(point)
                patchRolList.append(point['value'])
                response.append(result)
        if len(patchAcqList) > 0 and len(patchVerList) > 0 and len(patchValList) > 0 and len(patchRolList) > 0:
            result = dict()
            result['name'] = 'Average'
            result['series'] = list()
            point = dict()
            avgPat = list(filter(None, patchAcqList))
            i = 0
            for x in avgPat:
                i += x  
            point['name'] = 'Patch Acquired'
            point['value'] = i / len(avgPat)
            result['series'].append(point)
            point = dict()
            avgVal = list(filter(None, patchValList))
            i = 0
            for x in avgVal:
                i += x
            point['name'] = 'Patch Validated'
            point['value'] = i / len(avgVal)
            result['series'].append(point)
            point = dict()
            avgVer = list(filter(None, patchVerList))
            i = 0
            for x in avgVer:
                i += x
            point['name'] = 'Patch Verified'
            point['value'] = i / len(avgVer)
            result['series'].append(point)
            point = dict()
            avgRol = list(filter(None, patchRolList))
            i = 0
            for x in avgRol:
                i += x
            point['name'] = 'Patch Rolled Out'
            point['value'] = i / len(avgRol)
            result['series'].append(point)
            response.append(result)
        return JsonResponse(response, safe=False)
@api_view(['GET'])
def vulnsByOs(request, days):
    if request.method == 'GET': 
        timedays = int(days)
        timedays = timedelta(days=timedays)
        timedays=datetime.now() - timedays
        sorted_response = list()
        vulns = vulnerability.objects.all().exclude(cpe='None').values_list('cpe').filter(dayZero__gte = timedays)
        cpeSet=list()
        response = list()
        for x in vulns:
            if x[0] != '': 
                wfns = x[0].split(" ")
                if len(wfns) > 0:
                    for y in range(0, len(wfns)):
                        try:
                            uri = CPE2_3(wfns[y])
                            if uri.get_part() == ['o']:
                                cpeSet.append([uri.get_vendor(), uri.get_product(), uri.get_version()])
                        except Exception as e:
                            print(e)
        while len(list(cpeSet)) > 0:
            result = dict()
            cpeStr = str()
            cpeStr= str(cpeSet[0][0])+": "+str(cpeSet[0][1])+"-"+str(cpeSet[0][2])
            strg = " ".join(cpeStr)
            strg = strg.replace(" ", "")
            val = cpeSet.count(cpeSet[0])
            cpeSet = [value for value in cpeSet if value != cpeSet[0]]
            result['name'] = strg
            result['value'] = val
            response.append(result) 
            sorted_response = sorted(response, key=lambda d: d['value'], reverse=True)
        return JsonResponse(sorted_response[:10], safe=False)
@api_view(['GET'])
def vulnsByApp(request, days):
    if request.method == 'GET': 
        timedays = int(days)
        timedays = timedelta(days=timedays)
        timedays=datetime.now() - timedays
        sorted_response = list()
        vulns = vulnerability.objects.all().exclude(cpe='None').values_list('cpe').filter(dayZero__gte = timedays)
        cpeSet=list()
        response = list()
        for x in vulns:
            if x[0] != '': 
                wfns = x[0].split(" ")
                if len(wfns) > 0:
                    for y in range(0, len(wfns)):
                        try:
                            uri = CPE2_3(wfns[y])
                            if uri.get_part() == ['a']:
                                cpeSet.append([uri.get_vendor(), uri.get_product(), uri.get_version()])
                        except Exception as e:
                            print(e)
        while len(list(cpeSet)) > 0:
            result = dict()
            cpeStr = str()
            cpeStr= str(cpeSet[0][0])+": "+str(cpeSet[0][1])+"-"+str(cpeSet[0][2])
            strg = " ".join(cpeStr)
            strg = strg.replace(" ", "")
            val = cpeSet.count(cpeSet[0])
            cpeSet = [value for value in cpeSet if value != cpeSet[0]]
            result['name'] = strg
            result['value'] = val
            response.append(result)
            sorted_response = sorted(response, key=lambda d: d['value'], reverse=True) 
        return JsonResponse(sorted_response[:10], safe=False)
@api_view(['GET'])
def vulnsByHardware(request, days):
    if request.method == 'GET':
        timedays = int(days)
        timedays = timedelta(days=timedays)
        timedays=datetime.now() - timedays
        sorted_response = list()
        vulns = vulnerability.objects.all().exclude(cpe='None').values_list('cpe').filter(dayZero__gte = timedays)
        cpeSet=list()
        response = list()
        for x in vulns:
            if x[0] != '': 
                wfns = x[0].split(" ")
                if len(wfns) > 0:
                    for y in range(0, len(wfns)):
                        try:
                            uri = CPE2_3(wfns[y])
                            if uri.get_part() == ['h']:
                                cpeSet.append([uri.get_vendor(), uri.get_product(), uri.get_version()])
                        except Exception as e:
                            print(e)
        while len(list(cpeSet)) > 0:
            result = dict()
            cpeStr = str()
            cpeStr= str(cpeSet[0][0])+": "+str(cpeSet[0][1])+"-"+str(cpeSet[0][2])
            strg = " ".join(cpeStr)
            strg = strg.replace(" ", "")
            val = cpeSet.count(cpeSet[0])
            cpeSet = [value for value in cpeSet if value != cpeSet[0]]
            result['name'] = strg
            result['value'] = val
            response.append(result)
            sorted_response = sorted(response, key=lambda d: d['value'], reverse=True) 
        return JsonResponse(sorted_response[:10], safe=False)
@api_view(['GET'])
def assetCPEBreakdown(request):
    if request.method == 'GET': 
        tags = asset.objects.all().values_list('tags')
        cpeSet=list()
        response = list()
        for x in tags:
            if x[0] != '' and isinstance(x[0], str): 
                wfns = x[0].split(",")
                if len(wfns) > 0:
                    for y in range(0, len(wfns)):
                        try:
                            uri = CPE2_3(wfns[y])
                            cpeSet.append([uri.get_vendor(), uri.get_product()])
                        except Exception as e:
                            pass
        while len(list(cpeSet)) > 0:
            result = dict()
            cpeStr = str()
            cpeStr= str(cpeSet[0][0])+": "+str(cpeSet[0][1])
            strg = " ".join(cpeStr)
            strg = strg.replace(" ", "")
            val = cpeSet.count(cpeSet[0])
            cpeSet = [value for value in cpeSet if value != cpeSet[0]]
            result['name'] = strg
            result['value'] = val
            response.append(result)
            sorted_response = sorted(response, key=lambda d: d['value'], reverse=True) 
        return JsonResponse(sorted_response, safe=False)
@api_view(['GET'])
def ticketsInProgBreakdown(request):
    if request.method == 'GET': 
        grouplist = ticket.objects.all().exclude(group__isnull=True).exclude(group='').values_list('group')
        grouplist = list(dict.fromkeys(grouplist))
        response = list()
        for x in grouplist:
            result = dict()
            result['name'] = x
            result['value'] = ticket.objects.filter(group = x[0]).count()
            response.append(result)
        return JsonResponse(response, safe=False)
@api_view(['GET'])
def vulnBreakdown(request):
    if request.method == 'GET': 
        affvulns = vulnerability.objects.all().exclude(assetid__isnull=True).values_list('mc', 'mi', 'ma', 'mav', 'ms')
        i=0
        j=0
        verlist = list()
        while(j < len(affvulns[0])):
            i=0
            vert =list()
            while ( i < len(affvulns)):
                vert.append(affvulns[i][j])
                i += 1
            j +=1
            verlist.append(vert)
        labels = ['Confidentiality Impact', 'Integrity Impact', 'Availability Impact', 'Attack Vector', 'Scope']
        response = list()
        for x in range (0, len(verlist)):
            result = dict()
            result['name'] = labels[x]
            result['series'] = list()
            while len(verlist[x]) > 0:
                point = dict()
                point['name'] = verlist[x][0]
                point['value'] = verlist[x].count(verlist[x][0])
                verlist[x] = [value for value in verlist[x] if value != verlist[x][0]]
                result['series'].append(point)
            response.append(result)
        return JsonResponse(response, safe=False)
@api_view(['GET', 'PUT', 'DELETE'])
def getUser(request, username):
    try:
        userN = User.objects.get(username=username)
        if request.method == 'GET': 
            user_serializer = UserSerializer(userN) 
            return JsonResponse(user_serializer.data)
        elif request.method == 'PUT': 
            user_data = JSONParser().parse(request) 
            user_serializer = UserSerializer(userN, data=user_data) 
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data) 
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE': 
            User.delete() 
            return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
def userList(request):
    if request.method == 'GET': 
        userL = User.objects.all().exclude(is_superuser=True)
        user_serializer = UserSerializer(userL, many=True)
        return JsonResponse(user_serializer.data, safe=False)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer  = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        print(user)
        print(JsonResponse(serializer.data, status=status.HTTP_200_OK))
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class ListUsers(APIView):

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return JsonResponse(usernames, status=status.HTTP_200_OK, safe=False)