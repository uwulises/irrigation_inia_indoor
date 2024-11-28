# Navigate to the directory containing your Python scripts
cd /home/rpi/irrigation_inia_indoor/data_mega_logger

python3 sistema_riego.py &
# Check if the first script executed successfully
if [ $? -eq 0 ]; then
  echo "subscriber ran successfully."
else
  echo "subscriber encountered an error."
  exit 1
fi