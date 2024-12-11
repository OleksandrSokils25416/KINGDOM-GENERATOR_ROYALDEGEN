from transformers import AutoModelForCausalLM, AutoTokenizer
from sagemaker.huggingface import HuggingFace
import logging

class KingdomStoriesTrainer:
    def __init__(self, model_name, dataset_s3_paths, role, huggingface_token):
        """
        Initialize the KingdomStoriesTrainer class.
        Args:
            model_name (str): Hugging Face model name to fine-tune.
            dataset_s3_paths (dict): S3 paths for training and validation datasets.
            role (str): AWS SageMaker execution role ARN.
            huggingface_token (str): Hugging Face API token.
        """
        self.model_name = model_name
        self.dataset_s3_paths = dataset_s3_paths
        self.role = role
        self.huggingface_token = huggingface_token
        self.trained_model_path = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    def fine_tune_model(self):
        """
        Fine-tune the model on the kingdom stories dataset using SageMaker.
        """
        try:
            # Define hyperparameters for fine-tuning
            hyperparameters = {
                'model_name_or_path': self.model_name,
                'train_file': self.dataset_s3_paths['train'],
                'validation_file': self.dataset_s3_paths['validation'],
                'output_dir': '/opt/ml/model',
                'do_train': True,
                'do_eval': True,
                'num_train_epochs': 3,
                'per_device_train_batch_size': 4,
                'save_steps': 500,
                'evaluation_strategy': 'steps',
                'logging_dir': '/opt/ml/output/logs',
            }

            # Create the SageMaker HuggingFace Estimator
            huggingface_estimator = HuggingFace(
                entry_point='run_clm.py',
                source_dir='./examples/pytorch/language-modeling',
                instance_type='ml.p3.2xlarge',
                instance_count=1,
                role=self.role,
                transformers_version='4.37.0',
                pytorch_version='2.1.0',
                py_version='py310',
                hyperparameters=hyperparameters
            )

            # Start the training job
            self.logger.info("Starting the training job...")
            huggingface_estimator.fit()

            # Save the trained model path
            self.trained_model_path = huggingface_estimator.model_data
            self.logger.info(f"Training completed. Model saved at: {self.trained_model_path}")

        except Exception as e:
            self.logger.error(f"Error during fine-tuning: {str(e)}")
            raise

    def push_model_to_hub(self, repo_name):
        """
        Push the fine-tuned model to the Hugging Face Hub.
        Args:
            repo_name (str): Name of the Hugging Face repository to upload the model to.
        """
        try:
            # Load the trained model and tokenizer
            self.logger.info("Loading the trained model...")
            model = AutoModelForCausalLM.from_pretrained(self.trained_model_path)
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)

            # Push the model and tokenizer to the Hugging Face Hub
            self.logger.info(f"Pushing the model to the Hugging Face Hub under: {repo_name}")
            model.push_to_hub(repo_name, use_auth_token=self.huggingface_token)
            tokenizer.push_to_hub(repo_name, use_auth_token=self.huggingface_token)
            self.logger.info(f"Model successfully pushed to: https://huggingface.co/{repo_name}")

        except Exception as e:
            self.logger.error(f"Error during model upload: {str(e)}")
            raise

    def run(self, repo_name):
        """
        Run the complete pipeline: fine-tune and push to Hugging Face Hub.
        Args:
            repo_name (str): Name of the Hugging Face repository for the fine-tuned model.
        """
        self.fine_tune_model()
        self.push_model_to_hub(repo_name)

if __name__ == "__main__":
    # AWS IAM role for SageMaker
    role = "arn:aws:iam::123456789012:role/sagemaker_execution_role"

    # Dataset paths on S3
    dataset_s3_paths = {
        'train': 's3://your-bucket-name/kingdom_stories_train.json',
        'validation': 's3://your-bucket-name/kingdom_stories_validation.json'
    }

    # Hugging Face API token
    huggingface_token = "hf_HugginFaceAPI"

    # Hugging Face model name and repo name
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    repo_name = "Longhill/kingdom-stories-custom-model"

    # Instantiate and run the trainer
    trainer = KingdomStoriesTrainer(
        model_name=model_name,
        dataset_s3_paths=dataset_s3_paths,
        role=role,
        huggingface_token=huggingface_token
    )
    trainer.run(repo_name=repo_name)
