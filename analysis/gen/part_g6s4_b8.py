DATA_B8 = {
"T837": {
"python": r"""
import threading
import time

the_list = []
list_lock = threading.Condition()

def run():
    with list_lock:
        for i in range(10):
            while not the_list:
                print("Consumer is waiting")
                list_lock.wait()
            k = the_list.pop(0)
            print("consume=" + str(k))
            list_lock.notify_all()
            time.sleep(0.5)
""",
"c": r"""
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

#define QUEUE_CAPACITY 64

static int queue[QUEUE_CAPACITY];
static int queue_size = 0;
static pthread_mutex_t list_m = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t list_c = PTHREAD_COND_INITIALIZER;

void run(void) {
    pthread_mutex_lock(&list_m);
    for (int i = 0; i < 10; i++) {
        while (queue_size == 0) {
            printf("Consumer is waiting\n");
            pthread_cond_wait(&list_c, &list_m);
        }
        int k = queue[0];
        for (int j = 1; j < queue_size; j++) queue[j - 1] = queue[j];
        queue_size--;
        printf("consume=%d\n", k);
        pthread_cond_broadcast(&list_c);
        usleep(500000);
    }
    pthread_mutex_unlock(&list_m);
}
""",
"csharp": r"""
using System;
using System.Collections.Generic;
using System.Threading;

public class Consumer
{
    private static readonly List<int> list = new List<int>();
    private static readonly object listLock = new object();

    public void Run()
    {
        lock (listLock)
        {
            for (int i = 0; i < 10; i++)
            {
                while (list.Count == 0)
                {
                    Console.WriteLine("Consumer is waiting");
                    Monitor.Wait(listLock);
                }
                int k = list[0];
                list.RemoveAt(0);
                Console.WriteLine("consume=" + k);
                Monitor.PulseAll(listLock);
                Thread.Sleep(500);
            }
        }
    }
}
"""
}
}
