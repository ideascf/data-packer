# 简介
json_getter是一个字段提取工具包。

- 服务提供端：预定义一系列的Getter对象，用于验证和转换服务请求端传入的json数据为内部可用的字典。
- 服务请求端：按照服务提供方要求的数据格式创建好Getter对象后，将请求的原始字典快捷方便的转为服务提供方需要的格式。

# 定义
* json_getter不是jsonschema，即不是一个json数据的验证器
* json_getter是字段提取的工具包，即完成从源字典中以一定规则获取需要的字段，并填充到目的字典。

# 组成
* Field类，用来定义字典中的各个字段。 如： MustField, OptionalField, PlaceholderField, DefaultField等
* Getter类，用于使用预定义的Field集合去完成数据的转换提取。
* Checker类，预定义一系列常用的Checker。 如：EmailChecker，MobileChecker等

# 应用场景
1. 微信支付业务中，封装到微信的请求数据，解析微信的返回数据。
2. web业务中，解析并转换浏览器传入的请求数据。
