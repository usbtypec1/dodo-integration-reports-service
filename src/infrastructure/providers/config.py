from typing import Annotated

from fast_depends import Depends

from bootstrap.config import Config, load_config_from_file

ConfigDependency = Annotated[Config, Depends(load_config_from_file)]
