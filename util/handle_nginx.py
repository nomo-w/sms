import os
from config import Nginx


class NginxApi:
    @staticmethod
    def reload_nginx():
        os.system('systemctl restart nginx')

    @staticmethod
    def delete_nginx_conf(file_name):
        os.remove(f'{Nginx.nginx_path}{file_name}')

    @classmethod
    def create_new_conf_file(cls, domain):
        data = Nginx.base_format % (domain, Nginx.index_path, Nginx.backend_path)
        file_name = f'{domain.split(".")[0]}.conf'
        with open(f'{Nginx.nginx_path}{file_name}', 'w') as f:
            f.write(data)
        cls.reload_nginx()
        return file_name

    @classmethod
    def update_conf_file(cls, domain, old_file_name):
        cls.delete_nginx_conf(old_file_name)
        data = Nginx.base_format % (domain, Nginx.index_path, Nginx.backend_path)
        file_name = f'{domain.split(".")[0]}.conf'
        with open(f'{Nginx.nginx_path}{file_name}', 'w') as f:
            f.write(data)
        cls.reload_nginx()
        return file_name