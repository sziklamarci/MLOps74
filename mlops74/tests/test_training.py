import subprocess
import os

def test_training_script():
    script_path = 'mlops74/smoke/train_model2.py'
    command = ['python', script_path]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check if the process exited successfully
    assert process.returncode == 0, f'Training script failed with error:\n{stderr.decode()}'

    # Check if the expected model checkpoint files are created
    last_checkpoint_path = 'mlops74/models/checkpoints/last.pth'
    best_checkpoint_path = 'mlops74/models/checkpoints/best.pth'
    
    print("Paths:")
    print(last_checkpoint_path)
    print(best_checkpoint_path)

    assert os.path.exists(last_checkpoint_path), f'Last model checkpoint file not found: {last_checkpoint_path}' # Run the tests from mlops74 directory
    assert os.path.exists(best_checkpoint_path), f'Best model checkpoint file not found: {best_checkpoint_path}' # Run the tests from mlops74 directory

if __name__ == '__main__':
    test_training_script()
