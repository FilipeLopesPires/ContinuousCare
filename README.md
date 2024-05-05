# ContinuousCare: your Personal Monitoring System

[Web Server](https://github.com/FilipePires98/ContinuousCare/tree/main/src/Server) | [Web Application](https://github.com/FilipePires98/ContinuousCare/tree/main/src/Client) | [Promotional Video](https://github.com/FilipePires98/ContinuousCare/blob/main/PromotionalVideo.mp4) | [Presentation](https://github.com/FilipePires98/ContinuousCare/blob/main/docs/presentations/Final_Presentation.pdf) | [Work Report](https://github.com/FilipePires98/ContinuousCare/blob/main/docs/reports/Final%20Report.pdf) | [MIE2020 Publication](https://ebooks.iospress.nl/publication/54133)

![Cover](https://github.com/FilipePires98/ContinuousCare/blob/main/docs/presentations/img/CoverSlide.png)

[![](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
![](https://img.shields.io/badge/Deployment-Docker-blue)
![](https://img.shields.io/badge/Platform-Web-blue)
![](https://img.shields.io/badge/Platform-Mobile-blue)
![](https://img.shields.io/badge/License-MIT-lightgrey)

## Description 

The proliferation of mobile devices for monitoring vital signs and physical activity is enhancing the emergence of a new healthcare paradigm. 
We suggest the integration of smart devices with air quality monitors in a personal healthcare system to answer some limitations of similar solutions. 
ContinuousCare is all about helping citizens better understand their health and body activity, aiding professional doctors with analysis tools and making available valuable data for external systems. 

We set out to support a data source of each nature and adopted a phylosophy of storage dedicated to temporal records in order to prove the concept of continuous health monitoring through easily available smart devices.
The intention was also to show the impact of the environment that people are exposed to on the symptons detected, so the air quality monitors were completed with a geolocation tracking service. This, along with a consideration for our users’ experiences and moods, denoted our means of tackeling this challenge.

ContinuousCare encompasses:

- A public REST API with 26 end-points, including the export of bulk anonymous data for analysis

- A Web Application supporting accounts for regular users and medical personnel, with dedicated analysis tools

- A Mobile Application serving not only as a GPS source, but also as an offline installation guide

- A system test-proven with a load of 100 users  while meeting all performance requirements

##  Repository Structure

/docs - work reports, presentations, diagrams, posters and more

/src - source code of the back-end server, the web and mobile applications and the relational and time-series databases

## Architecture 

<img src="https://github.com/FilipePires98/ContinuousCare/blob/main/docs/diagrams/architecture/Architecture.png" width="360px">

<img src="https://github.com/FilipePires98/ContinuousCare/blob/main/docs/diagrams/implementation/Implementation.png" width="480px">

## Supported Devices 

<p float="left">
  <img src="https://github.com/FilipePires98/ContinuousCare/blob/main/docs/presentations/img/FitbitCharge3.jpg" width="240px">
  <img src="https://github.com/FilipePires98/ContinuousCare/blob/main/docs/presentations/img/Foobot.jpg" width="240px">
</p>

[Fitbit Charge 3](https://www.fitbit.com/global/eu/home) | [Foobot](https://foobot.io/)

## Authors

The authors of this repository are André Pedrosa, Filipe Pires and João Alegria, and the project was developed for the Informatics Project Course of the licenciate's degree in Informatics Engineering of the University of Aveiro.

For further information, please contact us through the corresponding author Filipe at fsnap@protonmail.com.

## Citation

Please cite [our work](https://ebooks.iospress.nl/publication/54133) if you use ContinuousCare.

```bib
@article{Pires2020,
    author = {Pires, Filipe and Pedrdosa, André and Alegria, João and Costa, Carlos},
    year = {2020},
    month = {06},
    pages = {103-107},
    title = {Clinico-Environmental System for Personal Monitoring},
    volume = {270},
    journal = {Studies in health technology and informatics},
    doi = {10.3233/SHTI200131}
}
```
