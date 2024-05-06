# Task trackers synchronizer

##  Description

Task Trackers Synchronizer is a personal application that enables users to synchronize tasks across various task trackers in a flexible manner.


###  Features

-     Conversion to Generic Issues + NoSQL Design: Simplifies the addition of external issue providers by converting tasks into a generic format and utilizing a NoSQL design for flexibility and scalability.

-   Rule-based Synchronization Algorithm: Offers customizable synchronization processes based on user-defined rules. This feature is particularly useful in scenarios where customer and developer organizations operate on different task trackers but require synchronization for specific projects while adhering to internal issue tracking conventions.

### Development features

-  Logging

-  Comprehensive Testing & Coverage

-  REST API support

-  Automatic API documentation

-  Pre-Commit Code Linting & Formatting


## Quality gates evaluation

- Progress on Quality Gates Automation

<<<<<<< Updated upstream
    - Continuous Integration (CI) Jobs:
        - Automated jobs organized by various quality gates:
            - **Code Quality**:
                - *flake8*: A Python linting tool for enforcing coding standards.
                - *Black*: Used to automatically format code according to PEP 8 standards.
                - *Pre-commit Hooks*: Ensures code quality standards are met before committing changes.
                - *Code Coverage*:
                    - *Unit Tests with pytest*: Utilizes pytest for unit testing, integrating with issue providers APIs and following Test-Driven Development (TDD) methodology.
                    - *Integration Tests with pytest*: Ensures synchronization of all issues and includes idempotent tests with rule synchronization.
                    - *End-to-End (e2e) Tests with docker-compose*: Conducts end-to-end testing in a Dockerized environment.
                - *Mutation Unit Tests with mutmut*: Evaluates test coverage by performing mutation testing.
            
            - **Security**:
                - *Semgrep with Bandit Ruleset*: Utilizes Semgrep with Bandit ruleset to identify common Python vulnerabilities.
                - *SonarCloud*: Performs cloud-based security quality gate evaluations.
                - *Docker Image Scan with Trivy*: Scans Docker images for vulnerabilities.
                - *ZAPROXY (DAST)*: Conducts Dynamic Application Security Testing (DAST) using ZAPROXY.

            - **Performance**:
                - *k6*: A tool for load testing and performance monitoring.
                - *Prometheus*: Used for monitoring and alerting.
=======
    - Automated CI jobs organized by various quality gates:
        - **Code Quality**:
            - *Code Coverage* - verified through the `coverage_gate` job. Its passing also presupposes successful passing of code style checks:
                - *Unit Tests with pytest*: Utilizes pytest for unit testing, integrating with issue providers APIs and following Test-Driven Development (TDD) methodology.
                - *Integration Tests with pytest*: Ensures synchronization of all issues and includes idempotent tests with rule synchronization.
            - *Code Style*:
                - *flake8*: A Python linting tool for enforcing coding standards.
                - *Black*: Used to automatically format code according to PEP 8 standards.
                - *Pre-commit Hooks*: Ensures code quality standards are met before committing changes.
        
        - **Security**:
            - *Docker Image Scan with Trivy*: Scans Docker images for vulnerabilities. Since Trivy image scan is performed at the end, its successful passing supposes completion of all security checks.
            - *Semgrep with Bandit Ruleset*: Utilizes Semgrep with Bandit ruleset to identify common Python vulnerabilities.
            - *SonarCloud*: Performs cloud-based security quality gate evaluations.

        - **Performance**:
            - *k6*: A tool for load testing and performance monitoring. **Performance Gate** job is used to ensure that the application fulfills performance requirements.
>>>>>>> Stashed changes

- Other Testing Techniques

    - **Mocks**:
        - *Mock Backend API*: Allows end-to-end testing with frontend without being blocked by frontend-related issues.
        - *Mock Issue Providers*: Avoids unnecessary API calls by simulating responses.
        - *Mock Database*: Tests components dependent on the database without accessing the actual database.


<<<<<<< Updated upstream
=======
    - *Performance observability*: Prometheus is used for monitoring and alerting. 

    - *Dynamic Application Security Testing* (DAST):  *ZAPROXY*: Conducts Dynamic Application Security Testing (DAST) using ZAPROXY.


>>>>>>> Stashed changes
##  Getting Started

Getting started developing with this template is pretty simple using docker and docker-compose.

```shell script
# Clone the repository
git clone git@github.com:TaskTrackersSynchronizer/task-trackers-synchronizer.git

# cd into project root
cd task-trackers-synchronizer

# Launch the project
docker-compose up
```

### Development

For the development purposes, you can run the backend locally as follows:
```bash
poetry install . 
poetry run uvicorn --host 127.0.0.1 --port 3434  app.main:api --reload
```

Afterwards, the project will be live at [http://localhost:3434](http://localhost:3434).

### Testing

In order to test and lint the project locally you need to install the poetry dependencies outlined in the pyproject.toml file.

If you have Poetry installed then it's as easy as running `poetry shell` to activate the virtual environment first and then `poetry install` to get all the dependencies.





## Documentation

FastAPI automatically generates documentation based on the specification of the endpoints you have written. You can find the docs at [http://localhost:5000/docs](http://localhost:5000/docs).







