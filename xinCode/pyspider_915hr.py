# !/usr/bin/env python
# -*- encoding: utf-8 -*-
import hashlib
import re

import time
from bs4 import BeautifulSoup
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    @every(minutes=5 * 24 * 60)
    def on_start(self):
        job_url_bg = 'http://www.915hr.com/job'
        self.crawl(job_url_bg, callback=self.jobnumpage)
        person_url_bg = 'http://www.915hr.com/personnel'
        self.crawl(person_url_bg, callback=self.pernumpage)
        jianzhi_url_bg = 'http://www.915hr.com/jianzhi'
        self.crawl(jianzhi_url_bg, callback=self.jianzhinumpage)

    @config(age=24 * 60 * 60)
    def pernumpage(self,response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        mes = obJect.find('ul', class_='pagination')
        num = mes.find_all('li')
        nums = []
        for x in num:
            nums.append(x.getText())
        totalpage = nums[-2]
        for i in range(1, int(totalpage) + 1):
            url = 'http://www.915hr.com/personnel?page={}'.format(i)
            self.crawl(url,callback=self.getResumeHtml)

    @config(age=24 * 60 * 60)
    def getResumeHtml(self,response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        mes = obJect.find_all('div', class_='personbghover')
        resumes = []
        for i in mes:
            url = i.a['href']
            resumes.append(url)
        self.crawl(resumes, callback=self.ResumeParseHtml)

    @config(age=24 * 60 * 60)
    def ResumeParseHtml(self,response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        resumes = {}
        serial_numbers = obJect.find('div', class_='presumehead')
        serial_number = serial_numbers.find('li', class_='left').getText().split('：')[1]
        last_loading = serial_numbers.find('li', class_='right').getText().split('：')[1]
        first = obJect.find('div', class_='frist')
        pic_url = re.findall(r'src="(.*?)"/>', str(first.find('li', class_='left')), re.S)[0]
        right = first.find('li', class_='right')
        mes = right.find_all('li')

        name = mes[0].getText().replace(' ', '').replace('\n', '')
        info = mes[1].getText().replace(' ', '').replace('\n', '')
        addres = mes[2].getText().replace(' ', '').split('\n')  # .replace('\n','')
        census_register = addres[1]
        NHom = addres[2]
        now_address = mes[3].getText().replace(' ', '').replace('\n', '')

        third = obJect.find('div', class_='third')
        news = third.find_all('dd')
        y = []
        for x in news:
            y.append(x.getText())
        wantJob = y[0]
        wantLocation = y[1]
        Expect_jobs = y[2]
        Job_status = y[3]
        resumes["serial_number"] = serial_number
        resumes["last_loading"] = last_loading
        resumes["pic_url"] = pic_url
        resumes["name"] = name
        resumes["info"] = info
        resumes["census_register"] = census_register
        resumes["nhom"] = NHom
        resumes["now_address"] = now_address
        resumes["want_job"] = wantJob
        resumes["want_location"] = wantLocation
        resumes["expect_jobs"] = Expect_jobs
        resumes["job_status"] = Job_status
        resumes["resume_id"] = hashlib.md5((str(serial_number) + str(time.time())).encode('utf-8')).hexdigest()
        resumes["crawler_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        infoOne = obJect.find_all("div", class_="third")

        if len(info) == 1:
            resumes['info_evaluation'] = "未填写"
            resumes['experience'] = "未填写"
            resumes['education_experience'] = "未填写"
            resumes['language_ability'] = "未填写"
            resumes["expertise"] = "未填写"
            resumes["certificate"] = "未填写"
            resumes["other_information"] = "未填写"
        if len(infoOne) > 1:
            for x in infoOne[1:]:
                if x.find("div", class_="title ico") != None:
                    info_evaluation = x.getText()
                    resumes["info_evaluation"] = info_evaluation
                else:
                    resumes['info_evaluation'] = "未填写"
                if x.find("div", class_="title ico2") != None:
                    experience = x.getText()
                    resumes["experience"] = experience
                else:
                    resumes['experience'] = "未填写"
                if x.find("div", class_="title ico3") != None:
                    Education_experience = x.getText()
                    resumes["education_experience"] = Education_experience
                else:
                    resumes['education_experience'] = "未填写"
                if x.find("div", class_="title ico5") != None:
                    Language_ability = x.getText()
                    resumes["language_ability"] = Language_ability
                else:
                    resumes['language_ability'] = "未填写"
                if "技能专长" in str(x):
                    expertise = x.getText()
                    resumes["expertise"] = expertise
                else:
                    resumes['expertise'] = "未填写"
                if "证书" in str(x):
                    certificate = x.getText()
                    resumes["certificate"] = certificate
                else:
                    resumes['certificate'] = "未填写"
                if "其它信息" in str(x):
                    Other_information = x.getText()
                    resumes["other_information"] = Other_information
                else:
                    resumes['other_information'] = "未填写"
        return resumes

    @config(age=24 * 60 * 60)
    def jobnumpage(self,response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        totalpage = obJect.find("div", class_='list3').getText().replace('\n', '').split('/')[1].replace('\n', '')
        everyPageUrlFirstPart = 'http://www.915hr.com/job?page='
        for i in range(1, int(totalpage) + 1):
            everyPageUrl = everyPageUrlFirstPart+str(i)
            self.crawl(everyPageUrl, callback=self.parseHtml)

    @config(age=24 * 60 * 60)
    def parseHtml(self,response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        infos = obJect.find_all('div', class_='saith')
        # print(info)
        # tmp = {}
        # jobs = []
        job_urls = []
        company_urls = []
        for info in infos:
            job_url = info.find('li', class_='list1').a['href']
            job_urls.append(job_url)
            company_url = info.find('li', class_='list4').a['href']
            company_urls.append(company_url)
            # salary = info.find('li', class_='list2').getText()
            # company = info.find('li', class_='list4').getText()
            # job = info.find('li', class_='list1').getText().replace('\n', '')
            # locationAndeducation = info.find('li', class_='list1 son_list2_refont').getText().replace(' ', '')
            # releaseTime = info.find('li', class_='list2 son_list2_refont').getText()
            # IndustryAndScale = info.find('li', class_='list4 son_list2_refont').getText().replace(' ', '')
            # socialBenefits = info.find('li', class_='list').getText()
            # tmp['jobs'] = job
            # tmp['job_url'] = job_url
            # tmp['salary'] = salary
            # tmp['company'] = company
            # tmp['company_url'] = company_url
            # tmp['locationAndeducation'] = locationAndeducation
            # tmp['releaseTime'] = releaseTime
            # tmp['IndustryAndScale'] = IndustryAndScale
            # tmp['socialBenefits'] = socialBenefits
            # jobs.append(tmp)
        company_urls = list(set(company_urls))
        self.crawl(company_urls, callback=self.companyParseHtml)
        job_urls = list(set(job_urls))
        self.crawl(job_urls, callback=self.jobParseHtml)

    @config(age=24 * 60 * 60)
    def companyParseHtml(self,response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        short_name = obJect.find('span', class_='brands').getText().replace('\n', '')
        full_names = obJect.find('div', class_='authenticate').p.getText().replace('\n', '').replace(' ',
                                                                                                     '')  # .split('\n')#.replace(' ','')
        sales_orientation = obJect.find('div', class_='authenticate').span.getText().replace('\n', '').replace(' ', '')
        print(full_names, sales_orientation)
        if len(full_names.split(sales_orientation)) == 2 and '' not in full_names.split(sales_orientation):
            certification_status = full_names.split(sales_orientation)[1]
            full_name = full_names.split(sales_orientation)[0]
        else:
            full_name = full_names.split(sales_orientation)[0]
            certification_status = '未认证'
        introduction = obJect.find('div', class_='content').getText().replace(' ', '')
        mess = obJect.find('div', class_='job_display_right')
        enterprise_property = obJect.find('div', class_='remark').getText().replace(' ', '').replace('\n', '')
        info = obJect.find('div', class_='temptation')
        social_benefitss = []
        nums = info.find_all('i')
        for item in nums:
            social_benefitss.append(item.getText())
        social_benefits = '|'.join(social_benefitss)
        try:
            company_source_id = re.findall(r'com_id=(.*?)"></div>',res,re.S)[0]
        except IndexError:
            company_source_id = 'Can Not Found company_source_id!'
        mes = mess.find_all('li', class_='right')
        companyIfon = {}
        if len(mes) == 5:
            ContactPerson = mes[0].getText().replace('\n', '')
            tel = mes[1].getText().replace('\n', '')
            virstUrl = mes[2].getText().replace('\n', '')
            email = mes[3].getText().replace('\n', '')
            address = mes[4].getText().replace('\n', '')
            companyIfon["short_name"] = short_name
            companyIfon["full_name"] = full_name
            companyIfon["sales_orientation"] = sales_orientation
            companyIfon["introduction"] = introduction
            companyIfon["contact_person"] = ContactPerson
            companyIfon["tel"] = tel
            companyIfon["virst_url"] = virstUrl
            companyIfon["email"] = email
            companyIfon["enterprise_property"] = enterprise_property
            companyIfon["address"] = address
            companyIfon['social_benefits'] = social_benefits
            companyIfon["company_id"] = hashlib.md5((str(short_name) + str(time.time())).encode('utf-8')).hexdigest()
            companyIfon["crawler_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            companyIfon["certification_status"] = certification_status
            companyIfon["company_source_id"] = company_source_id
        else:
            pass
        if companyIfon == {}:
            return 'ERROR IN companyParseHtml FUNCTION'
        else:
            return companyIfon

    @config(age=24 * 60 * 60)
    def jobParseHtml(self,response):
        res = response.text
        try:
            job_source_id = re.findall(r'job_id=(.*?)"></div>',res,re.S)[0]
        except IndexError:
            job_source_id = 'Can Not Found company_source_id job_source_id!'
        job_info = {}
        obJect = BeautifulSoup(res, 'lxml')
        jobs = obJect.find('span', class_='left-title').h1.getText()
        salary = obJect.find('span', class_='left-title').p.getText()
        detailedAddress = re.findall(r'<em>(.*?)</em>', str(obJect.find('span', class_='job-info').p), re.S)[0]
        info = obJect.find('ul', class_='job-list')
        ners = re.findall(r'<em>(.*?)</em>', str(info), re.S)
        Department = ners[0]
        count = ners[1]
        DegreeRequirement = ners[2]
        WorkExperience = ners[3]
        gender = ners[4]
        age = ners[5]
        uploader = obJect.find('div', class_='advisory').getText().replace('\n', '')
        publisher_contact = obJect.find('div', class_='publisher-contact').getText().\
            replace('\n', '').replace('[ 查看 ]','')
        Response_rates = obJect.find_all('span', class_='work-efficiency')[0].h3.getText()
        lastLoading = obJect.find_all('span', class_='work-efficiency')[1].h3.getText()
        describe = obJect.find('div', class_='describe').getText()
        welfaresmes = obJect.find('span', class_='job-welfare')
        welfaresinfo = welfaresmes.find_all('i')
        welfareslist = []
        for item in welfaresinfo:
            welfareslist.append(item.getText())
        welfare = '|'.join(welfareslist)
        belong_companys = obJect.find('div', class_='job_display_right border')
        infos = belong_companys.find('li', class_='title').a['href']#.getText().replace(' ', '').replace('\n', '')

        try:
            belong_company = re.findall(r'comabout_(.*?).html', infos, re.S)[0][6:]
        except IndexError:
            belong_company = 'Can Not Found belong_company!'

        job_info["title"] = jobs
        job_info["salary"] = salary
        job_info["detailed_address"] = detailedAddress
        job_info["department"] = Department
        job_info["count"] = count
        job_info["degree_requirement"] = DegreeRequirement
        job_info["work_experience"] = WorkExperience
        job_info["gender"] = gender
        job_info["age"] = age
        job_info["uploader"] = uploader
        job_info["publisher_contact"] = publisher_contact
        job_info["response_rates"] = Response_rates
        job_info["last_loading"] = lastLoading
        job_info["describe"] = describe
        job_info["jobs_nature"] = "全职"
        job_info["job_id"] = hashlib.md5((str(publisher_contact) + str(time.time())).encode('utf-8')).hexdigest()
        job_info["crawler_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        job_info['welfare'] = welfare
        job_info['belong_company'] = belong_company
        job_info['job_source_id'] = job_source_id
        return job_info

    @config(age=24 * 60 * 60)
    def jianzhinumpage(self,response):
        res = response.text
        totalpage = re.findall(r'index/sign(.*?).jpg"', res, re.S)
        li = map(lambda x: int(x), totalpage)
        page = max(li)
        for i in range(1,page+1):
            jianzhi_url = 'http://www.915hr.com/jianzhi?type_id=0&city_id=&salary_method=0&page={}'.format(i)
            self.crawl(jianzhi_url, callback=self.getjianzhiHtml)

    @config(age=24 * 60 * 60)
    def getjianzhiHtml(self, response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')
        jianzhi = obJect.find_all('span', class_='jobName')
        urlList = []
        for item in jianzhi[1:]:
            print(item)
            urlList.append(item.a['href'])
        self.crawl(urlList, callback=self.PartParseHtml)

    @config(age=24 * 60 * 60)
    def PartParseHtml(self, response):
        res = response.text
        obJect = BeautifulSoup(res, 'lxml')

        time_job = {}

        info = obJect.find('div', class_='baseInfo')

        title = info.h2.span.getText()
        date = info.h2.find('span', class_='date').getText()
        salary = info.find('div', class_='salary').getText()
        time_job["title"] = title
        time_job["date"] = date
        time_job["salary"] = salary
        details = info.ul.find_all('li')
        detail = []
        for i in details:
            detail.append(i.find_all('span')[1].getText().replace(' ', ''))
        time_job["numbers"] = detail[0]
        time_job["location"] = detail[1]
        time_job["workspace"] = detail[2]
        time_job["valid_term"] = detail[3]

        workTime = info.find_all('tr')

        Am = re.findall(r'class="(.*?)"></td>', str(workTime[1]), re.S)
        Pm = re.findall(r'class="(.*?)"></td>', str(workTime[2]), re.S)
        Night = re.findall(r'class="(.*?)"></td>', str(workTime[3]), re.S)
        scheduling = {"Monday": [Am[0], Pm[0], Night[0]],
                      "Tuesday": [Am[1], Pm[1], Night[1]],
                      "Wednesday": [Am[2], Pm[2], Night[2]],
                      "Thursday": [Am[3], Pm[3], Night[3]],
                      "Friday": [Am[4], Pm[4], Night[4]],
                      "Saturday": [Am[5], Pm[5], Night[5]],
                      "Sunday": [Am[6], Pm[6], Night[6]]
                      }
        time_job["scheduling"] = scheduling

        part_detail = obJect.find('div', class_='details')

        publisher = part_detail.find('p', class_='p1').getText().split('：')[1]
        publisher_tel = part_detail.find('p', class_='p2').getText().replace(' ', '').replace('\r', '').replace(
            '\n\xa0\xa0\xa0\xa0\xa0', '')
        time_job["publisher"] = publisher
        time_job["publisher_tel"] = publisher_tel

        jobDescribes = part_detail.find('div', class_='jobDescribe')  # .getText()
        data = jobDescribes.find_all('p')
        education = data[0].getText().split('：')[1]
        gender = data[1].getText().split('：')[1]
        position_statement = data[3].getText()
        compInfo = part_detail.find('div', class_='compInfo').getText()
        time_job["education"] = education
        time_job["gender"] = gender
        time_job["position_statement"] = position_statement
        time_job["comp_info"] = compInfo
        time_job["jobs_nature"] = "兼职"
        companyBasic = obJect.find('div', class_='company')
        other = companyBasic.find_all('li')
        companyName = companyBasic.find('div', class_='name').getText().replace('\n', '')
        industry = re.findall(r'</span>(.*?)</li>', str(other[0]), re.S)[0]
        Nature_of_Business = re.findall(r'</span>(.*?)</li>', str(other[1]), re.S)[0]
        companyscale = re.findall(r'</span>(.*?)</li>', str(other[2]), re.S)[0].replace('人', '')
        time_job["companyn_name"] = companyName
        time_job["industry"] = industry
        time_job["nature_of_business"] = Nature_of_Business
        time_job["companyscale"] = companyscale
        time_job["part_id"] = hashlib.md5((str(gender) + str(time.time())).encode('utf-8')).hexdigest()
        time_job["crawler_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return time_job






































































