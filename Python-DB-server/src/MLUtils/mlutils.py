import joblib

class AssetDiscoveryModel:

    def __init__(self):
        self.model = AdaptiveRandomForestClassifier()

    def save_model(self, file_path="./preTrainedModel/preTrainedModel.joblib"):
        joblib.dump(self.model, file_path)

    # Example: load_model("./preTrainedModel/preTrainedModel.joblib")
    def load_model(self, filePath="./preTrainedModel/preTrainedModel.joblib"):    
        return joblib.load(filePath)
    
    def train(self):    
        
    def update(self):
        
    def predict(self):