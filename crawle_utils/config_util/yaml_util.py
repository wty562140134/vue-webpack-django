import yaml


class YamlLoadUtil:
    """
    yaml配置文件读取类
    """

    def __init__(self, file_path, use_loader='FullLoader'):
        """
        构造函数
        :param file_path: 配置文件路径(包括文件名)
        :type file_path:str
        :param use_loader: 需要使用的yaml的loader默认为FullLoader,
        还有('BaseLoader', 'FullLoader', 'SafeLoader', 'Loader', 'UnsafeLoader')
        :type use_loader:str
        """
        self._file_path = file_path
        self._use_loader = use_loader

    def open_yaml(self):
        """
        打开yaml配置文件函数
        :return: 配置文件数据对象
        """
        with open(self._file_path, 'r', encoding='UTF-8') as config_file:
            config_obj = yaml.load(config_file, Loader=eval('yaml.{}'.format(self._use_loader)))
            # config_obj = yaml.load_all(config_file, Loader=eval('yaml.{}'.format(self._use_loader)))
        return config_obj

    def get_config_data(self, config_keys=None):
        """
        获取配置文件中配置的数据
        :param config_keys: 配置文件中数据的key默认为None
        :type config_keys:str
        :return: 配置文件中的数据,为None时则返回整个配置文件中的数据
        """
        config_data = self.open_yaml()
        if config_keys is None:
            return config_data
        return config_data[config_keys]


# if __name__ == '__main__':
#     """
#     用法demo
#     """
#     y = YamlLoadUtil('./demo.yaml')
#     data = y.get_config_data('apple')
#     data1 = y.get_config_data()
#     print(y.get_config_data()['dog'])
#     print(data1)
#     print(data)
