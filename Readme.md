# ExpertGPT

<div align="center">
    <img src="./ExpertGPT.svg" alt="ExpertGPT-logo" width="30%"  style="border-radius: 0%; padding-bottom: 20px"/>
</div>

## Getting Started 🚀

### Prerequisites 📋

Ensure you have the following installed:

- Docker
- Docker Compose
- Qdrant
- Zep

Additionally, you'll need a [Supabase](https://supabase.com/) account for:

- Creating a new Supabase project
- Supabase Project API key
- Supabase Project URL

### Installation Steps 💽

- **Step 1**: Clone the repository using **one** of these commands:

  - If you don't have an SSH key set up:

  ```bash
  git clone https://gitlab.com/lambda-vision/expertgpt.git && cd ExpertGPT
  ```

  - If you have an SSH key set up or want to add it ([guide here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account))

  ```bash
  git clone git@gitlab.com:lambda-vision/expertgpt.git && cd ExpertGPT
  ```

- **Step 2**: Copy the `.XXXXX_env` files

  ```bash
  cd expertgpt
  cp .backend_env.example backend/.env
  cp .frontend_env.example frontend/.env
  ```

- **Step 3**: Update the `backend/.env` and `frontend/.env` file

  > _Your `supabase_service_key` can be found in your Supabase dashboard under Project Settings -> API. Use the `anon` `public` key found in the `Project API keys` section._

  > _Your `JWT_SECRET_KEY`can be found in your supabase settings under Project Settings -> API -> JWT Settings -> JWT Secret_

  > _The `NEXT_PUBLIC_BACKEND_URL` is set to localhost:5050 for the docker. Update it if you are running the backend on a different machine._

  > _The `ENCODER_MODEL`can be selected `all-MiniLM-L6-v2` or others_

  > _`ZEP_API_URL` is zep server url. If you installed zep server locally, you can set it localhost:8000_

  > _`PROXYCURL_API_KEY` can be found in proxycurl site._
  - [ ] Change variables in `backend/.env`
  - [ ] Change variables in `frontend/.env`

- **Step 4**: Use the `migration.sh` script to run the migration scripts

  ⚠️Not completed

- **Step 5**: Launch the app

  ```bash
  docker compose up --build
  ```

  You can run individual components by following:
  - ExpertGPT
  ```bash
  cd expertgpt
  docker compose -f docker-compose.dev.yml up --build
  ```

  - OpenAPI Document
  ```bash
  cd openapi-test
  docker compose up
  ```

  - Qdrant
  ```bash
  docker pull qdrant/qdrant  # Download qdrant
  docker run -p 6333:6333 \
      -v $(pwd)/qdrant_storage:/qdrant/storage:z \
      qdrant/qdrant
  ```

  - Zep
  ```bash
  cd zep
  docker-compose up
  ```
- **Step 6**: Navigate to `localhost:3000` in your browser

