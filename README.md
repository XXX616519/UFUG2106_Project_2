# UFUG_2106_Project_2

<a id="readme-top"></a>

## 👥 Contributors

[<img src="https://github.com/XXX616519.png" width="80" alt="XXX616519" />](https://github.com/XXX616519)
[<img src="https://github.com/Altairpaca.png" width="80" alt="Altairpaca" />](https://github.com/Altairpaca)
[<img src="https://github.com/jyi664.png" width="80" alt="jyi664" />](https://github.com/jyi664)
[<img src="https://github.com/MoliaiELS.png" width="80" alt="MoliaiELS" />](https://github.com/MoliaiELS)




<!-- PROJECT LOGO -->
<br />
<div align="center">

<h1 align="center">Text Encryption and Decryption using Cryptography
Algorithms</h1>

  <p align="center">
    <br />
    <a href="https://github.com/XXX616519/UFUG2106_Project_2"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/XXX616519/UFUG2106_Project_2">View Demo</a>
    &middot;
    <a href="https://github.com/XXX616519/UFUG2106_Project_2">Report</a>
    &middot;
    <a href="https://github.com/XXX616519/UFUG2106_Project_2">Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary><span style="font-size: 18px;"><b>📑 Table of Contents</b></span></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

### 📂File Structure
```
DSAA2031_Final_Project/
├── .vscode/                
│   └── settings.json
├── main/
|   ├── data/
|       ├── input_file/
|           └── testpicture.png
|       ├── output_file/
|           └── restored.png
|       ├── data.txt
|       ├── decrypt.txt
|       └── encrypt.txt      
|   └── run/             
|       ├── Decrypt.py
|       ├── Encrypt.py
|       ├── Restore.py
|       └── Turn_Into_Bytes.py
├── src/
|       ├── ElGamal/
|           └── ElGamal.py
|       └── RSA/
|           ├── rsa.py
|           └── unittest_rsa.py
├── Group Project 2 Assessment Rubrics-1.pdf                 
├── Perf&Sec_Analysis.md            
└── UFUG2106_project2.pdf                  
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### 🧑‍💻 Programming Languages & Tools

* [![SQL][SQL]][SQL-url]
* [![Python][Python]][Python-url]
* [![JavaScript][JavaScript]][JavaScript-url]
* [![HTML][HTML]][HTML-url]
* [![CSS][CSS]][CSS-url]
* [![Git][Git]][Git-url]
* [![GitHub][GitHub]][GitHub-url]
* [![Flask][Flask]][Flask-url]
* [![Django][Django]][Django-url]
* [![Node.js][Node.js]][Node.js-url]
* [![Express.js][Express.js]][Express.js-url]
* [![VSCode][VSCode]][VSCode-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
---

## 🚀 Getting Started

This is a guide to help you set up the project locally using **HTML**, **CSS**, **JavaScript**, **Python**, and **SQL**. Follow the steps below to get a local development environment up and running.

---

### 📋 Prerequisites

Make sure you have the following installed:

* **Python 3.8+**: [Install Python](https://www.python.org/downloads/)
* **Node.js & npm** (for JavaScript frontend build tools): [Install Node.js](https://nodejs.org/)
* **A Web Browser** (Chrome/Edge/Firefox)
* **SQLite** or **MySQL** (for SQL support)

---

### 🛠️ Installation Steps

1. **Clone the repository**

   ```sh
   git clone https://github.com/XXX616519/DSAA2031_Final_Project.git
   cd DSAA2031_Final_Project
   ```

2. **Set up the Python backend**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the SQL database**

   MySQL only:

   ```sh
   python init_database.py  # Initialize database schema and data
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

   > Enter your MySQL username and password as prompted. The script will automatically create the payroll database and import schema/data.

4. **Install JavaScript dependencies (optional, for frontend development only)**

   ```sh
   cd server
   npm install
   ```

5. **Run the Node.js backend server**

   ```sh
   python start_server.py
   ```

6. **Open the frontend pages**

   * Open client/index.html, student.html, teacher.html, or admin.html directly in your browser.

---

### ✅ Done!

You're now ready to start working with:

* `HTML` for structure
* `CSS` for styling
* `JavaScript` for interactivity
* `Python` for backend logic
* `SQL` for data storage

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## 📖Report

Use this space to show the report of our project. 
Please refer to the [Documentation](https://github.com/XXX616519/DSAA2031_Final_Project/blob/main/report/functions.md)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## 💬Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## 📬 Contact

| Name          | Email                                                |
|---------------|------------------------------------------------------|
| Keyu HU(SQL and Report)       | [khu616@connect.hkust-gz.edu.cn](mailto:khu616@connect.hkust-gz.edu.cn)     |
| Zhouan SHEN(Client)   | [zshen575@connect.hkust-gz.edu.cn](mailto:zshen575@connect.hkust-gz.edu.cn) |
| Zhenzhuo LI(Server)   | [zli743@connect.hkust-gz.edu.cn](mailto:zli743@connect.hkust-gz.edu.cn)     |
| Yingwen PENG(Client)  | [ypeng996@connect.hkust-gz.edu.cn](mailto:ypeng996@connect.hkust-gz.edu.cn) |

**Project Link**: [DSAA2031_Final_Project](https://github.com/XXX616519/DSAA2031_Final_Project)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[SQL]: https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=mysql&logoColor=white
[SQL-url]: https://en.wikipedia.org/wiki/SQL

[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[JavaScript]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript

[HTML]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML

[CSS]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS

[Git]: https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white
[Git-url]: https://git-scm.com/

[GitHub]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[GitHub-url]: https://github.com/

[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/

[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/

[Node.js]: https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white
[Node.js-url]: https://nodejs.org/

[Express.js]: https://img.shields.io/badge/Express.js-404D59?style=for-the-badge&logo=express&logoColor=white
[Express.js-url]: https://expressjs.com/

[VSCode]: https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white
[VSCode-url]: https://code.visualstudio.com/

[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
