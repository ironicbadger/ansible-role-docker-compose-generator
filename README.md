# ansible-role-docker-compose-generator

Pass this role a hash and it will generate a docker-compose.yml file. The following structure is supported and is designed to be passed to the role using `group_vars`.

Rendered files are output to the `output` directory.

```
---

# global vars
global_env_vars:
  - "PUID=1313"
  - "PGID=1313"
appdata_path: /opt/appdata
container_config_path: /config
container_data_path: /data

# container definitions
containers:
  - service_name: letsencrypt
    active: true
    image: linuxserver/letsencrypt
    container_name: le
    ports:
      - 80:80
      - 443:443
    volumes:
      - "{{ appdata_path }}/letsencrypt/config:{{ container_config_path }}"
    restart: always
    depends_on:
      - unifi
      - nextcloud
      - quassel
    include_global_env_vars: true
    environment:
      - EMAIL=email@email.com
      - URL=some.tld
      - SUBDOMAINS=nc, irc, unifi
      - ONLY_SUBDOMAINS=true
      - DHLEVEL=4096
      - TZ=Europe/London
      - VALIDATION=http
    mem_limit: 256m
  - service_name: nextcloud
    active: true
    image: nextcloud
    container_name: nextcloud
    include_global_env_vars: false
    volumes:
      - "{{ appdata_path }}/nextcloud/html:/var/www/html"
      - "{{ appdata_path }}/nextcloud/apps:/var/www/html/custom_apps"
      - "{{ appdata_path }}/nextcloud/config:/var/www/html/config"
      - "{{ appdata_path }}/nextcloud/data:/var/www/html/data"
      - "{{ appdata_path }}/nextcloud/theme:/var/www/html/themes"
    mem_limit: 256m
    restart: "{{ unless_stopped }}"
    ports:
      - "8081:80"
  - service_name: unifi
    active: true
    image: linuxserver/unifi
    container_name: unifi
    mem_limit: 512m
    volumes:
      - "{{ appdata_path }}/unifi:{{ container_config_path }}"
    depends_on:
      - service: mongodb
        condition: service_started
    include_global_env_vars: true
    restart: "{{ unless_stopped }}"
  - service_name: quassel
    active: true
    image: linuxserver/quassel
    container_name: quassel
    include_global_env_vars: true
    volumes:
      - "{{ appdata_path }}/quassel:{{ container_config_path }}"
    mem_limit: 128m
    ports:
      - "4242:4242"
  - service_name: service-on-custom-network
    active: true
    image: ubuntu:24.04
    container_name: example
    include_global_env_vars: true
    networks:
      my-network:
      my-network-2:
  - service_name: service-on-custom-network-wit-hardcoded-ip
    active: true
    image: ubuntu:24.04
    container_name: example-hardcoded
    include_global_env_vars: true
    networks:
      my-network:
        ipv4_address: 172.16.0.1

# optionally include networks to be created (these can be referenced using the networks key in the container definition above)
networks:
  - network_name: my-network
    driver: bridge
    ipam:
      config:
        - subnet: 172.16.0.0/24
  - network_name: my-network-2
    driver: bridge
    ipam:
      config:
        - subnet: 172.16.1.0/24
```
