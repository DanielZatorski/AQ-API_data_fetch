# AQ-API_Data_Fetch

This repository is designed to demonstrate the process of creating a simple and low cost noSQL database (DynamoDB) using AWS services as well as OpenAQ API.

## Skills & Tools Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-FF6C37?style=for-the-badge&logo=appveyor&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white)


## Project Overview

### OpenAQ API
Parameters for fetching data can be found in the API documentation. Please refer to the [OpenAQ API Documentation](https://docs.openaq.org/docs/introduction).

### AWS
AWS Lambda is set to trigger every hour with the help of AWS EventBridge to write data to DynamoDB. Policies used in .json format can be found in this repository.

## Requirements

- Python 3.11

## Repository Structure

- **src/**: Contains the source code for fetching data and writing to DynamoDB.
- **policies/**: Contains .json format policies used by AWS
- **README.md**: This file.


