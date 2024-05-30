import tkinter as tk
from tkinter import messagebox, ttk
import time
import random

def format_memory_state(memory, frames):
    memory_str = " ".join(f"[{page}]" for page in memory + [''] * (frames - len(memory)))
    return memory_str

def fifo_page_replacement(pages, frames):
    """
    FIFO Page Replacement Algorithm:
    - Simple and easy to implement.
    - The oldest page in memory is replaced first.
    - Performance can suffer due to the "Belady's Anomaly," where adding more frames can lead to more page faults.
    """
    start_time = time.time()
    physical_memory = []
    page_faults = 0
    movements = []
    iterations = 0

    for page in pages:
        iterations += 1
        if page not in physical_memory:
            if len(physical_memory) < frames:
                physical_memory.append(page)
            else:
                physical_memory.pop(0)
                physical_memory.append(page)
            page_faults += 1
        movements.append(physical_memory.copy())

    end_time = time.time()
    run_time = end_time - start_time

    return page_faults, physical_memory, movements, run_time, iterations

def lru_page_replacement(pages, frames):
    """
    LRU Page Replacement Algorithm:
    - More complex than FIFO but generally performs better.
    - Replaces the least recently used page.
    - Requires keeping track of page access history, which can be costly in terms of time and space.
    - Avoids Belady's Anomaly.
    """
    start_time = time.time()
    physical_memory = []
    page_faults = 0
    movements = []
    page_indices = {}
    iterations = 0

    for i, page in enumerate(pages):
        iterations += 1
        if page not in physical_memory:
            if len(physical_memory) < frames:
                physical_memory.append(page)
            else:
                # Find the least recently used page
                lru_page = min(physical_memory, key=lambda p: page_indices[p])
                physical_memory.remove(lru_page)
                physical_memory.append(page)
            page_faults += 1
        else:
            # Move the page to the end to mark it as most recently used
            physical_memory.remove(page)
            physical_memory.append(page)
        
        # Update the index of the current page
        page_indices[page] = i
        movements.append(physical_memory.copy())

    end_time = time.time()
    run_time = end_time - start_time

    return page_faults, physical_memory, movements, run_time, iterations

def optimal_page_replacement(pages, frames):
    """
    Optimal Page Replacement Algorithm:
    - Theoretically provides the best performance with the least page faults.
    - Replaces the page that will not be used for the longest period of time in the future.
    - Not feasible in practice because it requires future knowledge of page references.
    - Useful as a benchmark to compare other algorithms.
    """
    start_time = time.time()
    physical_memory = []
    page_faults = 0
    movements = []
    iterations = 0

    for i, page in enumerate(pages):
        iterations += 1
        if page not in physical_memory:
            if len(physical_memory) < frames:
                physical_memory.append(page)
            else:
                future_pages = pages[i + 1:]
                farthest_index = -1
                page_to_replace = None
                for f in physical_memory:
                    if f not in future_pages:
                        page_to_replace = f
                        break
                    else:
                        index = future_pages.index(f)
                        if index > farthest_index:
                            farthest_index = index
                            page_to_replace = f
                physical_memory.remove(page_to_replace)
                physical_memory.append(page)
            page_faults += 1
        movements.append(physical_memory.copy())

    end_time = time.time()
    run_time = end_time - start_time

    return page_faults, physical_memory, movements, run_time, iterations

def validate_input(pages, frames):
    if not pages:
        messagebox.showerror("Input Error", "Please enter a valid page string.")
        return False
    if not frames.isdigit() or int(frames) <= 0:
        messagebox.showerror("Input Error", "Please enter a valid number of frames.")
        return False
    return True

def on_submit():
    pages = entry_pages.get().strip().split()
    frames = entry_frames.get().strip()
    if not validate_input(pages, frames):
        return
    
    frames = int(frames)
    algorithm = algorithm_var.get()

    if algorithm == "FIFO":
        page_faults, final_frames, movements, run_time, iterations = fifo_page_replacement(pages, frames)
    elif algorithm == "LRU":
        page_faults, final_frames, movements, run_time, iterations = lru_page_replacement(pages, frames)
    elif algorithm == "Optimal":
        page_faults, final_frames, movements, run_time, iterations = optimal_page_replacement(pages, frames)

    result_text = f"Page Faults: {page_faults}\nFinal Physical Memory: {final_frames}\n\nMemory Movements:\n"
    for state in movements:
        result_text += f"{format_memory_state(state, frames)}\n"
    result_text += f"\nAlgorithm: {algorithm}\nRun Time: {run_time:.6f} seconds\nIterations: {iterations}"

    result_box.config(state=tk.NORMAL)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, result_text)
    result_box.config(state=tk.DISABLED)

    update_visuals(pages, frames, movements)
    show_large_input_results(frames)

def update_visuals(pages, frames, movements):
    # Clear previous visualizations
    for widget in virtual_memory_frame.winfo_children():
        widget.destroy()
    for widget in page_table_frame.winfo_children():
        widget.destroy()
    for widget in physical_memory_frame.winfo_children():
        widget.destroy()

    # Display Virtual Memory
    tk.Label(virtual_memory_frame, text="Virtual Memory").grid(row=0, column=0)
    for i, page in enumerate(pages):
        tk.Label(virtual_memory_frame, text=f"Page {i}: {page}").grid(row=i+1, column=0, padx=5, pady=2)

    # Display Page Table
    tk.Label(page_table_frame, text="Page Table").grid(row=0, column=0)
    page_table = {page: f"Frame {i}" if i < frames else "Not in Memory" for i, page in enumerate(movements[-1])}
    for i, (page, frame) in enumerate(page_table.items()):
        tk.Label(page_table_frame, text=f"Page {page}: {frame}").grid(row=i+1, column=0, padx=5, pady=2)

    # Display Physical Memory
    tk.Label(physical_memory_frame, text="Physical Memory").grid(row=0, column=0)
    for i, page in enumerate(movements[-1]):
        tk.Label(physical_memory_frame, text=f"Frame {i}: {page}").grid(row=i+1, column=0, padx=5, pady=2)

def show_large_input_results(frames):
    large_pages = [random.randint(0, 100) for _ in range(10000)]
    fifo_faults, _, _, fifo_time, fifo_iters = fifo_page_replacement(large_pages, frames)
    lru_faults, _, _, lru_time, lru_iters = lru_page_replacement(large_pages, frames)
    optimal_faults, _, _, optimal_time, optimal_iters = optimal_page_replacement(large_pages, frames)
    
    large_result_text = f"\n\nPerformance with Large Random Input (10000 pages):\n"
    large_result_text += f"FIFO Page Faults: {fifo_faults}, Run Time: {fifo_time:.6f} sec\n"
    large_result_text += f"LRU Page Faults: {lru_faults}, Run Time: {lru_time:.6f} sec\n"
    large_result_text += f"Optimal Page Faults: {optimal_faults}, Run Time: {optimal_time:.6f} sec\n"
    
    result_box.config(state=tk.NORMAL)
    result_box.insert(tk.END, large_result_text)
    result_box.config(state=tk.DISABLED)


# Setting up the main window
root = tk.Tk()
root.title("Page Replacement Algorithms with Virtual and Physical Memory")

# Labels and Entries for Page Input and Frame Input
tk.Label(root, text="Enter page string (space-separated):").grid(row=0, column=0, padx=10, pady=5)
entry_pages = tk.Entry(root)
entry_pages.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Enter number of frames:").grid(row=1, column=0, padx=10, pady=5)
entry_frames = tk.Entry(root)
entry_frames.grid(row=1, column=1, padx=10, pady=5)

# Dropdown menu for algorithm selection
algorithm_var = tk.StringVar(root)
algorithm_var.set("FIFO")  # default value
tk.Label(root, text="Select algorithm:").grid(row=2, column=0, padx=10, pady=5)
algorithm_menu = tk.OptionMenu(root, algorithm_var, "FIFO", "LRU", "Optimal")
algorithm_menu.grid(row=2, column=1, padx=10, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result Display Box
result_box = tk.Text(root, height=15, width=50, state=tk.DISABLED)
result_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Frame for algorithm characteristics
characteristics_frame = tk.Frame(root)
characteristics_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)


# Frames for visual representation
virtual_memory_frame = tk.Frame(root)
virtual_memory_frame.grid(row=6, column=0, padx=10, pady=10)

page_table_frame = tk.Frame(root)
page_table_frame.grid(row=6, column=1, padx=10, pady=10)

physical_memory_frame = tk.Frame(root)
physical_memory_frame.grid(row=6, column=2, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()
