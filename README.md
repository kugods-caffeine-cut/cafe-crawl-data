# 카페아웃 백엔드
**설명 :** 카페인 섭취 기록 앱 카페아웃 백엔드-데이터 레포지토리입니다.


**작성일자 :** 2023.01.22



## 목표 및 현황

- **목표 :**
  - **22년 Q3 : 카페 데이터 크롤링 통해 DB 구축 / API 서버 배포 / API 명세서 작성**
  - **22년 Q4 : 중복 데이터 이슈, API서버 관련 유지 보수**
- **현황 :**
  - **23년 Q1 : 회원 관리 시스템 및 JWT 기반 통신 체계 개발**

## 구성


- **cafe-crawl-data** : 카페 정보 웹 크롤링 및 DB Upload 코드
  - `source/` : 카페 크롤링 코드
    - 기술 : `Python` / `Selenium` / `BeautifulSoup4`
  - `drink-data/` : 크롤링 한 데이터 json 형태로 적재
  - `db-controller/` : NodeJS 기반 크롤링 데이터 파싱 및 DB Upsert 코드
    - 기술 : `NodeJS` , `File I/O`

## 개발팀원

- **KUGODS 1기 개발 코어 김규민**  
  [![GitHub Badge](https://img.shields.io/badge/GitHub-181717?&logo=GitHub&logoColor=white&style=for-the-badge&link=https://github.com/KY00KIM)](https://github.com/KY00KIM)
- **KUGODS 1기 개발 크루 이성진**  
  [![GitHub Badge](https://img.shields.io/badge/GitHub-181717?&logo=GitHub&logoColor=white&style=for-the-badge&link=https://github.com/mobius29)](https://github.com/mobius29)
- **KUGODS 1기 개발 크루 김백규**  
  [![GitHub Badge](https://img.shields.io/badge/GitHub-181717?&logo=GitHub&logoColor=white&style=for-the-badge&link=https://github.com/centneuf0109)](https://github.com/centneuf0109)

- **KUGODS 1기 개발 크루 정혜정**  
  [![GitHub Badge](https://img.shields.io/badge/GitHub-181717?&logo=GitHub&logoColor=white&style=for-the-badge&link=https://github.com/Hyejeong33h)](https://github.com/Hyejeong33h)

### 커밋 규칙
커밋 메세지는 다음과 같은 형식으로 작성합니다.
```
Activity: Commit Message
```

- Activities
  - `int`: only for initial commit
  - `doc`: changes document or comment
  - `ftr`: add new feature
  - `mod`: modify existing feature
  - `fix`: fix an error or issue
  - `rfc`: refactor code
  - `add`: add new file or directory
  - `rmv`: remove existing file or directory
- Example
  - `int: initial commit`
  - `add: prettier and eslint`
  - `rfc: refactoring code by prettier`
