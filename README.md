# 📊 Luxury Loan Portfolio Dashboard

This project demonstrates how to build and run a **Plotly Dash** dashboard application using **Docker Compose** in a cloud environment like **Play With Docker (PWD)**.
The application loads `LuxuryLoanPortfolio.csv` data and displays a summary and visualizations of the loan portfolio.

## 📂 Project Structure

    docker_plotly/
    ├── data/
    │   └── LuxuryLoanPortfolio.csv  # Data used by the dashboard
    ├── Dockerfile                   # Instructions for building the Dash (Python) image
    ├── Task_2.ipynb                 # Development notebook (optional)
    ├── Task_2.py                    # Main Plotly Dash application file
    ├── docker-compose.yml           # Configuration for running the Dash container
    └── requirements.txt             # Python dependencies (Pandas, Dash, Plotly, etc.)

--> Push this folder and all project files (including `docker-compose.yml`, `LuxuryLoanPortfolio.csv`, and Task_2.py) to a GitHub repository.

## ⚙️ 1. Environment Setup

These steps are performed in a terminal environment such as **Play With Docker (PWD)**.

1.  Open [Play with Docker](https://labs.play-with-docker.com/) and start a new instance.
2.  Clone the repository from GitHub:

    ```bash
    git clone [https://github.com/riansp/docker_plotly](https://github.com/riansp/docker_plotly)
    cd docker_plotly
    ```
---

## 🐳 2. Run Docker Compose

This command will build the Docker image (`--build`) based on the `Dockerfile` and run the container in detached mode (`-d`).

```bash
docker compose up -d --build

Ensure the crm_dash container is running and port 8050 is mapped:

```bash
docker ps

Expected output:

CONTAINER ID... IMAGE... COMMAND... STATUS... PORTS
... crm_dash  "python Task_2.py" Up X seconds 0.0.0.0:8050->8050/tcp crm_dash

## 🚀 3. Access the Plotly Dash Dashboard
    The Dash application runs on Port 8050 inside the container. Since you are using PWD, access must be done via the hostname exposed by PWD.

    1. Check Application Logs:
        Ensure the Plotly Dash application is running and listening on 0.0.0.0:
        
        ```bash
        docker logs crm_dash

        Expected output: Dash is running on http://0.0.0.0:8050/

    2. Open Port in PWD:
        -> In the PWD web interface (above the terminal), click the 8050 badge that appears, or click the "OPEN PORT" button and enter 8050.
        -> The browser will open a new tab with a long URL (e.g., ipXXX-...-8050.direct.labs.play-with-docker.com).

    3. Access the Dashboard (MUST USE HTTP):
        If the browser shows an error like "doesn't support a secure connection with HTTPS", your browser is enforcing a secure connection (HTTPS).
        ACTION REQUIRED: Manually change the protocol in the address bar from https:// to http://, then press Enter.
        Tip: If this still fails, try opening the http:// URL in an Incognito/Private Window.


## 🧹 4. Stop and Clean Up

``bash
  docker compose down

------------------------------------------------------------------------

## ✅ Workflow Summary in PWD
1. Clone the GitHub repository (git clone ...).
2. Build and run the container (docker compose up -d --build).
3. Check container status and logs (docker ps, docker logs crm_dash).
4. Access the dashboard via the exposed Port 8050 (must use http:// protocol).
5. Stop the environment (docker compose down).