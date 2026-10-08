# Master + 2 Workers Setup

This setup runs one master with 2 workers on the local network, each with a partition of the dataset (5,100, 4,950, and 4,950 samples).

## Files
- `master.py` - Master node that coordinates predictions
- `worker.py` - Worker node (used by both workers)
- `data.csv`, `data2.csv`, `data3.csv` - Partitioned datasets
- `label.csv`, `label2.csv`, `label3.csv` - Partitioned labels
- `start_workers.bat` - Start both workers on ports 5000 and 5001
- `run_master.bat` - Run master with 2 workers

## Usage

1. Start both workers:
   ```
   start_workers.bat
   ```

2. In a new terminal, run the master:
   ```
   run_master.bat
   ```

## Manual Usage

Start Worker 1:
```
python worker.py 1 5000
```

Start Worker 2:
```
python worker.py 2 5001
```

Run master:
```
python master.py http://localhost:5000,http://localhost:5001 "5.1,3.5,1.4,0.2"
```

## Network Configuration

For multi-machine setup, update the worker URLs in the master command with actual IP addresses:
```
python master.py http://192.168.1.20:5000,http://192.168.1.30:5000 "5.1,3.5,1.4,0.2"
```
