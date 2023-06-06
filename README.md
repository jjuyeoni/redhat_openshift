# 다인책 (다음 인생 책)
- 기간 : 2018.07 ~ 2018.11
- 성과 : 레드햇 코딩페스트 우수상 수상
- 팀원 총 3명

## 1.프로젝트 환경설정
- WBS 일정관리 + git 이용하여 협업
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/56eb816c-eae5-499a-9fa6-96ce1d318035)

## 2.프로젝트 주요기능
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/fd7eb612-23a1-4a5e-bcb0-de5547b94027)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/ce07f9bf-70f9-4290-91a8-4410dac25b7c)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/7aabc9eb-31fd-4a75-9b20-9bb978e74574)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/ee8a5730-a037-47d3-93cb-0a0e0aa1b115)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/915d6bd3-ccb3-4658-b9f2-f13def2d01fe)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/c7eba6f0-1f8e-4369-a63f-5cfc56780dac)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/64ef4d06-5c4d-4c99-969d-1c6e8a64c96c)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/ed65da5e-a243-46dc-a09e-9ec9b1a7a36d)

## 3.오픈시프트 배포 과정
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/d2606b43-704c-40ec-9735-d8c0ca21e5fe)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/fc397609-66cf-47ba-9c52-2b68b660c668)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/0d9abc13-f959-4e32-a4c8-ec9f20e44b09)
![image](https://github.com/jjuyeoni/redhat_openshift/assets/18046663/260915ad-cd74-4a5c-8962-392893aba48f)

## 4.프로젝트 내 역할
1. Django를 이용하여 웹서비스 개발
2. 카카오 도서정보 API 사용 및 yes24 베스트셀러 크롤링 하여 책 정보 추출
3. 자연어 토크나이저로 추출한 정보에서 명사 /형용사 추출을 통해 추천 알고리즘 생성
4. OAuth 이용한 구글 API 연동 로그인 개발
5. docker에 mysql 이미지 생성하여 openshift에 이미지 deploy

## 5. 프로젝트 진행 중 어려웠던 점
1. stop Words 정의
2. tf-idf의 적절한 feature값 정의
3. docker에 mysql 생성 후, workbench에 연결하여 table 형성하고 commit까지 한 다음에 hub에 올리는 과정에서 오류 발생.
