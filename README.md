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
    <a href="https://github.com/XXX616519/UFUG2106_Project_2/blob/main/test/result.md">View test result</a>
    &middot;
    <a href="https://github.com/XXX616519/UFUG2106_Project_2/blob/main/UFUG2106_Project_2_Group10.pdf">Report</a>
    &middot;
    <a href="https://github.com/XXX616519/UFUG2106_Project_2/blob/main/Perf%26Sec_Analysis.md">Analysis</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

### 📂File Structure
```
UFUG_2106_Project_2/
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
|   ├── ElGamal/
|       └── ElGamal.py
|   └── RSA/
|       ├── rsa.py
|       └── unittest_rsa.py
├── test/ # visualization
|   ├── brief_test.py
|   ├── data.txt
|   ├── elgamal_key_generate_time_graph.py
|   ├── encrypt_time_and_memory.py
|   ├── long_text_time_and_memory.py
|   ├── result.md
|   └── rsa_key_generate_time_graph.py
├── Group_Project2_Assessment_Rubrics-1.pdf               
├── Perf&Sec_Analysis.md # Analysis
├── README.md  
├── requirements.txt
├── UFUG2106_Project_2_Group10.pdf            
└── UFUG2106_project2.pdf                  
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### 🧑‍💻 Programming Languages & Tools

* [![Python][Python]][Python-url]
* [![HTML][HTML]][HTML-url]
* [![Git][Git]][Git-url]
* [![GitHub][GitHub]][GitHub-url]
* [![VSCode][VSCode]][VSCode-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
---

## 🚀 Getting Started

This is a guide to help you run this project locally using **Python**. Follow the steps below to get a local development environment up and running.

---

### 📋 Prerequisites

Make sure you have the following installed:

* **Python 3.8+**: [Install Python](https://www.python.org/downloads/)

---

### 🛠️ Installation Steps

1. **Clone the repository**

   ```sh
   git clone https://github.com/XXX616519/UFUG2106_Project_2
   cd UFUG2106_Project_2
   ```

2. **Set up the Python**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **File format requirement**

    ```
    TEXT: .txt  
    AUDIO: .mp3  
    PICTURE: .png  
    VIDEO: .mp4
    ```
4. **Input and Output location**

   ```
   main\data\input_file
   main\data\output_file
   ```

5. **Encrypt**

   ```sh
   python main\run\Turn_Into_Bytes.py
   python main\run\Encrypt.py
   ```

6. **Decrypt**

   ```sh
   python main\run\Decrypt.py
   python main\run\Restore.py
   ```
7. **Test and Visualization**
   ```sh
   python main\test\encrypt_time_and memory.py
   python main\test\long_text_time_and_memory.py
   python main\test\rsa_key_generate_time_graph.py 
   python main\test\elgamal_key_generate_time_graph.py
   ```
---

### ✅ Done!

### You're now ready to start!

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## 📖Report

Use this space to show the report of our project. 
Please refer to the [Documentation](https://github.com/XXX616519/UFUG2106_Project_2)

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

| Name                   | Email                                                                       |
|------------------------|-----------------------------------------------------------------------------|
| Ye GUO(RSA)            | [yguo704@connect.hkust-gz.edu.cn](mailto:yguo704@connect.hkust-gz.edu.cn)   |
| Keyu HU(ElGamal)       | [khu616@connect.hkust-gz.edu.cn](mailto:khu616@connect.hkust-gz.edu.cn)     |
| Jingyang YI(Test)      | [jyi664@connect.hkust-gz.edu.cn](mailto:jyi664@connect.hkust-gz.edu.cn)     |
| Zhenzhuo LI(Analysis)  | [zli743@connect.hkust-gz.edu.cn](mailto:zli743@connect.hkust-gz.edu.cn)     |

**Project Link**: [UFUG2106_Project_2](https://github.com/XXX616519/UFUG2106_Project_2)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[HTML]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML

[Git]: https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white
[Git-url]: https://git-scm.com/

[GitHub]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[GitHub-url]: https://github.com/

[VSCode]: https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white
[VSCode-url]: https://code.visualstudio.com/

[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
