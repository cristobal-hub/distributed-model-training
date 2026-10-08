import requests
from collections import Counter
import sys
import time
import json

print("MASTER STARTING...")

# Get worker addresses from command line or use default localhost
if len(sys.argv) > 1:
    workers = sys.argv[1].split(',')
else:
    workers = [
        "http://localhost:5000"
    ]

def predict(sample, simulate_failure=None):
    """
    Predict with optional node failure simulation
    simulate_failure: list of worker indices to fail (0-based), or 'random' for random failure
    """
    print("Sending request to workers...")
    if simulate_failure:
        print(f"SIMULATING FAILURE: {simulate_failure}")
    
    predictions = []
    worker_times = []
    start_time = time.time()

    for i, worker in enumerate(workers):
        # Check if this worker should fail
        should_fail = False
        if simulate_failure == 'random':
            import random
            should_fail = random.random() < 0.3  # 30% chance of failure
        elif isinstance(simulate_failure, list) and i in simulate_failure:
            should_fail = True
        
        if should_fail:
            print(f"SIMULATED FAILURE: Worker {i+1} ({worker}) - skipping")
            worker_times.append(None)
            continue
            
        try:
            print(f"Contacting {worker}...")
            worker_start = time.time()
            res = requests.post(worker + "/predict", json={"data": sample}, timeout=5)
            worker_elapsed = time.time() - worker_start
            worker_times.append(worker_elapsed)
            print(f"Response received in {worker_elapsed:.3f}s:", res.text)

            pred = res.json()['prediction']
            predictions.append(pred)

        except Exception as e:
            print(f" Error with {worker} →", e)
            worker_times.append(None)

    total_time = time.time() - start_time
    
    if not predictions:
        print(" No workers responded!")
        return None, None, None

    final = Counter(predictions).most_common(1)[0][0]
    return final, total_time, worker_times


try:
    # Accept sample data from command line or prompt for input
    if len(sys.argv) > 2:
        sample = [float(x) for x in sys.argv[2].split(',')]
        print(f"Using sample: {sample}")
    else:
        print("Enter Iris flower features:")
        sepal_length = float(input("Sepal length: "))
        sepal_width = float(input("Sepal width: "))
        petal_length = float(input("Petal length: "))
        petal_width = float(input("Petal width: "))
        sample = [sepal_length, sepal_width, petal_length, petal_width]

    labels = ["Setosa", "Versicolor", "Virginica"]
    
    # Check for failure simulation argument
    simulate_failure = None
    if len(sys.argv) > 3:
        if sys.argv[3] == 'random':
            simulate_failure = 'random'
        else:
            simulate_failure = [int(x) for x in sys.argv[3].split(',')]

    result, total_time, worker_times = predict(sample, simulate_failure)

    if result is not None:
        print("\n" + "="*50)
        print("PERFORMANCE METRICS")
        print("="*50)
        print(f"Total prediction time: {total_time:.3f}s")
        print(f"Number of workers: {len(workers)}")
        print(f"Workers responded: {len([t for t in worker_times if t is not None])}")
        print("\nIndividual worker times:")
        for i, (worker, wtime) in enumerate(zip(workers, worker_times)):
            if wtime is not None:
                print(f"  Worker {i+1} ({worker}): {wtime:.3f}s")
            else:
                print(f"  Worker {i+1} ({worker}): FAILED")
        print("="*50)
        print(f"Final Prediction: {labels[result]}")
        print("="*50)
        
        # Save metrics to file for visualization
        metrics = {
            "total_time": total_time,
            "num_workers": len(workers),
            "workers_responded": len([t for t in worker_times if t is not None]),
            "worker_times": worker_times,
            "prediction": result,
            "sample": sample
        }
        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        print("\nMetrics saved to metrics.json")

except Exception as e:
    print(" CRASH:", e)