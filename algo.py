import Algorithmia
import joblib
import numpy as np
import pandas as pd
import xgboost

model_path = "data://asli/xgboost_demo/musicalreviews_xgb_model.pkl"
client = Algorithmia.client()
model_file = client.file(model_path).getFile().name
loaded_xgb = joblib.load(model_file)

# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(input):
    series_input = pd.Series([input])
    result = loaded_xgb.predict(series_input)
    # Returning the first element of the list, as we'll be taking a single input for our demo purposes
    # As you'll see while building the model: 0->negative, 1->positive
    return {"sentiment": result.tolist()[0]}
