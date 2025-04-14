# 10b [Individual/Pairs/Group] Migrate from One Database to Another

**Type**: Individual/Pairs/Group

You are allowed to work in pairs or groups of three for this assignment if you find that easier and less work.

Create a migration script that migrates data from one database to another. You can choose any two databases you like. They can be different paradigms or even the same paradigm.



### **Docker and Docker-Compose Commands**

- Start the MySQL container in detached mode:
  ```bash
  docker-compose up -d
  ```

- Rebuild the containers after making changes to the `docker-compose.yaml` file:
  ```bash
  docker-compose up -d --build
  ```

- Stop the running containers:
  ```bash
  docker-compose down
  ```

- Stop the running containers and remove associated volumes:
  ```bash
  docker-compose down -v
  ```

- Connect to the MySQL database from within the container:
  ```bash
  docker exec -it <database_container_name> mysql -u root -prootpassword
  ```