#-*- coding:utf-8 -*-
# Author : 7secondsFish
# Data : 18-8-29 上午10:44
import requests
from bs4 import BeautifulSoup
import re
from store import *
url = 'http://www.915hr.com/comabout_06656e1592.html'
#urls = ['http://www.915hr.com/jobinfo_e9484711620.html','http://www.915hr.com/jobinfo_c97bc17632.html','http://www.915hr.com/jobinfo_c781139045.html']

res = requests.get(url).text
obJect = BeautifulSoup(res, 'lxml')
try:
    company_source_id = re.findall(r'com_id=(.*?)"></div>', res, re.S)[0]
except IndexError:
    company_source_id = 'Can Not Found company_source_id!'
print(company_source_id)



# job_info = {}
# jobs = obJect.find('span',class_='left-title').h1.getText().replace('\n','')
# salary = obJect.find('span',class_='left-title').p.getText()
# detailedAddress = re.findall(r'<em>(.*?)</em>',str(obJect.find('span',class_='job-info').p),re.S)[0]
# info = obJect.find('ul',class_='job-list')
# ners = re.findall(r'<em>(.*?)</em>',str(info),re.S)
# Department = ners[0]
# count = ners[1]
# DegreeRequirement = ners[2]
# WorkExperience = ners[3]
# gender = ners[4]
# age = ners[5]
# #print(ners)
# uploader = obJect.find('div',class_='advisory').getText().replace('\n','')
# publisher_contact = obJect.find('div',class_='publisher-contact').getText().replace('\n','').replace('[ 查看 ]','')
#
# Response_rates = obJect.find_all('span',class_='work-efficiency')[0].h3.getText()
# lastLoading = obJect.find_all('span',class_='work-efficiency')[1].h3.getText()
# describe = obJect.find('div',class_='describe').getText()
# #print(describe)
#
# welfaresmes = obJect.find('span',class_='job-welfare')
# welfaresinfo = welfaresmes.find_all('i')
# welfareslist = []
# for item in welfaresinfo:
#     welfareslist.append(item.getText())
# welfare = '|'.join(welfareslist)
# belong_companys = obJect.find('div',class_='job_display_right border')
# belong_company = belong_companys.find('li',class_='title').a.getText().replace(' ','').replace('\n','')
#
#
# job_info['jobs'] = jobs
# job_info['salary'] = salary
# job_info['detailedAddress'] = detailedAddress
# job_info['Department'] = Department
# job_info['count'] = count
# job_info['DegreeRequirement'] = DegreeRequirement
# job_info['WorkExperience'] = WorkExperience
# job_info['gender'] = gender
# job_info['age'] = age
# job_info['uploader'] = uploader
# job_info['publisher_contact'] = publisher_contact
# job_info['Response_rates'] = Response_rates
# job_info['lastLoading'] = lastLoading
# job_info['describe'] = describe
# job_info['welfare'] = welfare
# job_info['belong_company'] = belong_company
# print(job_info)

# # time_job = {}
# #
# # info = obJect.find('div', class_='baseInfo')
# #
# # title = info.h2.span.getText()
# # date = info.h2.find('span', class_='date').getText()
# # salary = info.find('div', class_='salary').getText()
# # time_job["title"] = title
# # time_job["date"] = date
# # time_job["salary"] = salary
# # details = info.ul.find_all('li')
# # detail = []
# # for i in details:
# #     detail.append(i.find_all('span')[1].getText().replace(' ', ''))
# # time_job["numbers"] = detail[0]
# # time_job["location"] = detail[1]
# # time_job["workspace"] = detail[2]
# # time_job["Valid_term"] = detail[3]
# #
# # workTime = info.find_all('tr')
# #
# # Am = re.findall(r'class="(.*?)"></td>', str(workTime[1]), re.S)
# # Pm = re.findall(r'class="(.*?)"></td>', str(workTime[2]), re.S)
# # Night = re.findall(r'class="(.*?)"></td>', str(workTime[3]), re.S)
# # scheduling = {"Monday": [Am[0], Pm[0], Night[0]],
# #               "Tuesday": [Am[1], Pm[1], Night[1]],
# #               "Wednesday": [Am[2], Pm[2], Night[2]],
# #               "Thursday": [Am[3], Pm[3], Night[3]],
# #               "Friday": [Am[4], Pm[4], Night[4]],
# #               "Saturday": [Am[5], Pm[5], Night[5]],
# #               "Sunday": [Am[6], Pm[6], Night[6]]
# #               }
# # time_job["scheduling"] = scheduling
# #
# # part_detail = obJect.find('div', class_='details')
# #
# # publisher = part_detail.find('p', class_='p1').getText().split('：')[1]
# # publisher_tel = part_detail.find('p', class_='p2').getText().replace(' ', '').replace('\r', '').replace(
# #     '\n\xa0\xa0\xa0\xa0\xa0', '')
# # time_job["publisher"] = publisher
# # time_job["publisher_tel"] = publisher_tel
# #
# # jobDescribes = part_detail.find('div', class_='jobDescribe')  # .getText()
# # data = jobDescribes.find_all('p')
# # education = data[0].getText().split('：')[1]
# # gender = data[1].getText().split('：')[1]
# # position_statement = data[3].getText()
# # compInfo = part_detail.find('div', class_='compInfo').getText()
# # time_job["education"] = education
# # time_job["gender"] = gender
# # time_job["position_statement"] = position_statement
# # time_job["compInfo"] = compInfo
# # time_job["jobs_nature"] = "兼职"
# # companyBasic = obJect.find('div', class_='company')
# # other = companyBasic.find_all('li')
# #
# # companyName = companyBasic.find('div', class_='name').getText().replace('\n', '')
# # industry = re.findall(r'</span>(.*?)</li>', str(other[0]), re.S)[0]
# # Nature_of_Business = re.findall(r'</span>(.*?)</li>', str(other[1]), re.S)[0]
# # companyscale = re.findall(r'</span>(.*?)</li>', str(other[2]), re.S)[0].replace('人', '')
# # time_job["companyName"] = companyName
# # time_job["industry"] = industry
# # time_job["Nature_of_Business"] = Nature_of_Business
# # time_job["companyscale"] = companyscale
# # time_job["_meta"] = {"store": "kafka", "collection": "crawler_part_qa"}
# # print(time_job)
# store = StoreWorker(resultdb = 'sdsfd',inqueue='sadsad')
# task = 'sadfd'
# store.on_result(task=task,result=job_info)





# resumes = {}
# serial_numbers = obJect.find('div',class_='presumehead')
# serial_number = serial_numbers.find('li',class_='left').getText().split('：')[1]
# last_loading = serial_numbers.find('li',class_='right').getText().split('：')[1]
# first = obJect.find('div',class_='frist')
# pic_url = re.findall(r'src="(.*?)"/>',str(first.find('li',class_='left')),re.S)[0]
# right = first.find('li',class_='right')
# mes = right.find_all('li')
#
# name = mes[0].getText().replace(' ','').replace('\n','')
# info = mes[1].getText().replace(' ','').replace('\n','')
# addres = mes[2].getText().replace(' ','').split('\n')#.replace('\n','')
# census_register = addres[1]
# NHom = addres[2]
# now_address = mes[3].getText().replace(' ','').replace('\n','')
#
# third = obJect.find('div',class_='third')
# news = third.find_all('dd')
# y= []
# for x in news:
#     y.append(x.getText())
# wantJob = y[0]
# wantLocation = y[1]
# Expect_jobs = y[2]
# Job_status = y[3]
# resumes['serial_number'] = serial_number
# resumes['last_loading'] = last_loading
# resumes['pic_url'] = pic_url
# resumes['name'] = name
# resumes['info'] = info
# resumes['census_register'] = census_register
# resumes['NHom'] = NHom
# resumes['now_address'] = now_address
# resumes['wantJob'] = wantJob
# resumes['wantLocation'] = wantLocation
# resumes['Expect_jobs'] = Expect_jobs
# resumes['Job_status'] = Job_status
#
# infoOne = obJect.find_all('div',class_='third')
# print('info',info)
#
# if len(info) == 1:
#     resumes['info_evaluation'] = "未填写"
#     resumes['experience'] = "未填写"
#     resumes['education_experience'] = "未填写"
#     resumes['language_ability'] = "未填写"
#     resumes["expertise"] = "未填写"
#     resumes["certificate"] = "未填写"
#     resumes["other_information"] = "未填写"
# if len(infoOne) > 1:
#     for x in infoOne[1:]:
#         if x.find("div", class_="title ico") != None:
#             info_evaluation = x.getText()
#             resumes["info_evaluation"] = info_evaluation
#         else:
#             resumes['info_evaluation'] = "未填写"
#         if x.find("div", class_="title ico2") != None:
#             experience = x.getText()
#             resumes["experience"] = experience
#         else:
#             resumes['experience'] = "未填写"
#         if x.find("div", class_="title ico3") != None:
#             Education_experience = x.getText()
#             resumes["education_experience"] = Education_experience
#         else:
#             resumes['education_experience'] = "未填写"
#         if x.find("div", class_="title ico5") != None:
#             Language_ability = x.getText()
#             resumes["language_ability"] = Language_ability
#         else:
#             resumes['language_ability'] = "未填写"
#         if "技能专长" in str(x):
#             expertise = x.getText()
#             resumes["expertise"] = expertise
#         else:
#             resumes['expertise'] = "未填写"
#         if "证书" in str(x):
#             certificate = x.getText()
#             resumes["certificate"] = certificate
#         else:
#             resumes['certificate'] = "未填写"
#         if "其它信息" in str(x):
#             Other_information = x.getText()
#             resumes["other_information"] = Other_information
#         else:
#             resumes['other_information'] = "未填写"
#
# print(resumes)





# job_info = {}
# jobs = obJect.find('span',class_='left-title').h1.getText().replace('\n','')
# salary = obJect.find('span',class_='left-title').p.getText()
# detailedAddress = re.findall(r'<em>(.*?)</em>',str(obJect.find('span',class_='job-info').p),re.S)[0]
# info = obJect.find('ul',class_='job-list')
# ners = re.findall(r'<em>(.*?)</em>',str(info),re.S)
# Department = ners[0]
# count = ners[1]
# DegreeRequirement = ners[2]
# WorkExperience = ners[3]
# gender = ners[4]
# age = ners[5]
# #print(ners)
# uploader = obJect.find('div',class_='advisory').getText().replace('\n','')
# publisher_contact = obJect.find('div',class_='publisher-contact').getText().replace('\n','').replace('[ 查看 ]','')
#
# Response_rates = obJect.find_all('span',class_='work-efficiency')[0].h3.getText()
# lastLoading = obJect.find_all('span',class_='work-efficiency')[1].h3.getText()
# describe = obJect.find('div',class_='describe').getText()
# print(describe)
# job_info['jobs'] = jobs
# job_info['salary'] = salary
# job_info['detailedAddress'] = detailedAddress
# job_info['Department'] = Department
# job_info['count'] = count
# job_info['DegreeRequirement'] = DegreeRequirement
# job_info['WorkExperience'] = WorkExperience
# job_info['gender'] = gender
# job_info['age'] = age
# job_info['uploader'] = uploader
# job_info['publisher_contact'] = publisher_contact
# job_info['Response_rates'] = Response_rates
# job_info['lastLoading'] = lastLoading
# job_info['describe'] = describe
# print(job_info)



















# short_name = obJect.find('span',class_='brands').getText().replace('\n','')
# full_names = obJect.find('div',class_='authenticate').p.getText().replace('\n','').replace(' ','')#.split('\n')#.replace(' ','')
# sales_orientation = obJect.find('div',class_='authenticate').span.getText().replace('\n','').replace(' ','')
# print(full_names,sales_orientation)
# if len(full_names.split(sales_orientation)) == 2 and '' not in full_names.split(sales_orientation):
#     certification_status = full_names.split(sales_orientation)[1]
#     full_name = full_names.split(sales_orientation)[0]
# else:
#     full_name = full_names.split(sales_orientation)[0]
#     certification_status = '未认证'
# #print(full_name)
# introduction = obJect.find('div',class_='content').getText().replace(' ','')
# mess = obJect.find('div',class_='job_display_right')
# mes = mess.find_all('li',class_='right')
# enterprise_property = obJect.find('div', class_='remark').getText().replace(' ','').replace('\n','')
# info = obJect.find('div', class_='temptation')
# social_benefitss = []
# nums = info.find_all('i')
# for item in nums:
#     social_benefitss.append(item.getText())
# social_benefits = '|'.join(social_benefitss)
#
# companyIfon = {}
# if len(mes) == 5:
#     ContactPerson = mes[0].getText().replace('\n','')
#     tel = mes[1].getText().replace('\n','')
#     virstUrl = mes[2].getText().replace('\n','')
#     email = mes[3].getText().replace('\n','')
#     address = mes[4].getText().replace('\n','')
#     companyIfon['ContactPerson'] = ContactPerson
#     companyIfon['tel'] = tel
#     companyIfon['virstUrl'] = virstUrl
#     companyIfon['email'] = email
#     companyIfon['short_name'] = short_name
#     companyIfon['address'] = address
#     companyIfon['social_benefitscompanyIfon["certification_status"] = certification_status'] = social_benefits
#     companyIfon["enterprise_property"] = enterprise_property
#     companyIfon["full_name"] = full_name
#     companyIfon["sales_orientation"] = sales_orientation
#
# else:
#     pass
#
# print(companyIfon)












































# infos = obJect.find_all('div', class_='saith')
#
# tmp = {}
# jobs = []
# job_urls = []
# company_urls = []
# for info in infos:
#     job = info.find('li',class_='list1').getText().replace('\n','')
#     job_url = info.find('li',class_='list1').a['href']
#     job_urls.append(job_url)
#     #status = info.find('li',class_='list1').a['em']
#     salary = info.find('li',class_='list2').getText()
#     company = info.find('li',class_='list4').getText().replace('\n','')
#     company_url = info.find('li',class_='list4').a['href']
#     company_urls.append(company_url)
#     locationAndeducation = info.find('li',class_='list1 son_list2_refont').getText().replace(' ','')
#     releaseTime = info.find('li',class_='list2 son_list2_refont').getText()
#     IndustryAndScale = info.find('li',class_='list4 son_list2_refont').getText().replace(' ','')
#     socialBenefits = info.find('li',class_='list').getText()
#     tmp['jobs'] = job
#     tmp['job_url'] = job_url
#     tmp['salary'] = salary
#     tmp['company'] = company
#     tmp['company_url'] = company_url
#     tmp['locationAndeducation'] = locationAndeducation
#     tmp['releaseTime'] = releaseTime
#     tmp['IndustryAndScale'] = IndustryAndScale
#     tmp['socialBenefits'] = socialBenefits
#     jobs.append(tmp)
# print(jobs)
# print('job_urls',len(job_urls))
# print('company_urls',len(company_urls))
# company_urls = list(set(company_urls))
# job_urls = list(set(job_urls))
# print(len(job_urls))
# print(len(company_urls))
# totalpage = obJect.find("div", class_='list3').getText().replace('\n','').split('/')[1].replace('\n','')
# print(totalpage)
#
# for i in range(1,int(totalpage)+1):
#     print(i)


if __name__ == '__main__':
    pass