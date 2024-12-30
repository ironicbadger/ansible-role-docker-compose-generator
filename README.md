# ansible-role-docker-compose-generator

This role will allow you to manage your docker-compose.yml file via Ansible (and be git-controlled).

## Role Variables

### Defaults:
```
docker_compose_generator_output_path: "~"
docker_compose_generator_uid: "1000"
docker_compose_generator_gid: "1000"
docker_compose_generator_config: |
  ChangeMe
```

### Global variables:

For some things, like setting UID/GID, or timezone, it's helpful to set them once and have them carry over to all containers.  Just as an example:

```
global_env_vars:
  - "UID={{ main_uid }}"
  - "GID={{ main_gid }}"
  - "PUID={{ main_uid }}"
  - "PGID={{ main_gid }}"
  - "TZ={{ ntp_timezone }}"
```

### Docker-Compose File

There are 2 ways to pass through your docker-compose file.  

#### Option 1
First is to define it in a template file, which can be done like this:

```
docker_compose_generator_config: "{{ lookup('template', 'roles/templates/docker-compose.yml.j2') }}"
```

If you have multiple hosts, you can even do something like this:
```
docker_compose_generator_config: "{{ lookup('template', 'roles/{{hostname}}templates/docker-compose.yml.j2') }}"
```
And put a docker-compose.yml.j2 file in ever host's template folder.

#### Option 2
The second option is to include a multiline string in your (somewhat similar to how this role use to work, but you would fully define the compose file).  Like this:

```
docker_compose_generator_config: |
  services:
    adguard:
      image: adguard/adguardhome:latest
      container_name: adguard
      cap_add:
        - NET_ADMIN
      volumes:
        - {{ appdata_path }}/adguard/conf:/opt/adguardhome/conf
        - {{ appdata_path }}/work:/opt/adguardhome/work
      ports:
        - 53:53/tcp
        - 53:53/udp
        - 853:853/tcp
        - 81:80/tcp
        - 444:443/tcp
        - 3000:3000/tcp
      restart: unless-stopped
```