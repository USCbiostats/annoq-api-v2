from pydantic import BaseModel

class ModelConfig(BaseModel):
    model_config = {
        "populate_by_name": True  # Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias. Defaults to False
    }