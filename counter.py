import thread
from Tkinter import *
import signal
from libs import trap
from libs import counter

def init_codes():
    code = list()
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.1.1"))                  #black_a4_copy
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.1.1"))                  #black_a3_copy
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.1.2"))                  #black_a4_print
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.1.2"))                  #black_a3_print
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.2.1"))                  #color_a4_copy
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.2.1"))                  #color_a4_print
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.2.2"))                  #color_a3_copy
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.2.2"))                  #color_a3_print
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.3.1.5.1"))                    #scan_a4
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.3.1.6.1"))                    #scan_a3
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.1.3.0"))                      #duplex
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.1.10.0"))                     #pages
    code.append(counter(".1.3.6.1.4.1.18334.1.1.1.5.7.2.1.8.0"))                      #originals
    return code

def get_all_delta():
    delta = list()
    for code in codes:
        delta.append(code.delta())
    return delta

def deltas_2_values(delta):
    values = list()
    values.append((delta[0] + delta[2]) - (2 * (delta[1] + delta[3])))  #BW A4
    values.append(delta[1] + delta[3])                                  #BW A3
    values.append((delta[4] + delta[6]) - (2 * (delta[5] + delta[7])))  #CL A4
    values.append(delta[5] + delta[7])                                  #CL A3
    values.append(delta[8] + delta[9])                                  #SCAN
    values.append(0)                                                    #D BW A4
    values.append(0)                                                    #D BW A3

    if delta[10] > 0:
        if (2 * delta[10]) == values[0]:
            values[0] = values[0] - (2 * delta[10])
            values[5] = delta[10]
        elif (2 * delta[10]) == values[0]:
            values[1] = values[1] - (2 * delta[10])
            values[6] = delta[10]

    ids = delta[12] - delta[11]          #originals - pages
    if ids > 0 and values[0] == delta[0]:
        values[0] = values[0] - (ids)
        values[5] = ids
    return values

def all_sum(values):
    global allsums
    for i in xrange(len(values)):
        allsums[i] += values[i]
    return allsums

def values_2_str(values):
    s = ""
    for i in xrange(len(values)):
        s += str(values[i]) + "\n"
    return s

def receive_signal(signum, stack):
    print "got signal"
    deltas = get_all_delta()
    job_vals = deltas_2_values(deltas)
    total_vals = all_sum(job_vals)
    updated_values = values_2_str(job_vals)
    updated_totals = values_2_str(total_vals)
    reset_job()
    #job_label.configure(text = updated_values)
    total_label.configure(text = updated_totals)

def receive_signal2(signum, stack):
    text = ["black_a4",
            "black_a3",
            "color_a4",
            "color_a3",
            "scan",
            "duplex_black_a4",
            "duplex_black_a3"]
    deltas = get_all_delta()
    values = deltas_2_values(deltas)
    for i in range(len(text)):
        print text[i], values[i]
    print "--------------------------------------"

def reset_button(event):
    reset_job()
    global allsums
    allsums = [0 for i in xrange(7)]
    updated_values = values_2_str(allsums)
    updated_totals = values_2_str(allsums)
    #job_label.configure(text = updated_values)
    total_label.configure(text = updated_totals)

def reset_job():
    for code in codes:
        code.job_reset()

def refresher():
    root.update_idletasks()
    root.after(1000, refresher)

def exit_gracefully(event):
    sys.exit(1)

codes = init_codes()
allsums = [0 for i in xrange(7)]
text  = "Black and White A4:\nBlack and White A3:\nColor A4:\n" \
        "Color A3:\nScan:\nDuplex Black and White A4:\nDuplex Black and White A3:"
try:
    thread.start_new_thread(trap, ())
except Exception, e:
    print e
    print "Error: unable to start thread"

signal.signal(signal.SIGUSR1, receive_signal)

root = Tk()
root.geometry("1440x900+0+0")
root.overrideredirect(True)
root.config(cursor='none')

text_label = Label(root, text=text, font=("Arial", 60), padx=80, pady=130, justify=RIGHT)
total_label = Label(root, text="0", font=("Arial", 60), padx=10, pady=130)

root.bind("<Button-1>", reset_button)
root.bind("<Shift_L>", exit_gracefully)
text_label.grid(row=1,column=0,sticky=N)
total_label.grid(row=1,column=2,sticky=N)

refresher()

root.mainloop()
