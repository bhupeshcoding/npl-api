# Error Documentation

## Error: Address Already in Use

When starting the API you might encounter the following error:

```
ERROR:    [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

### Explanation

This error occurs when the port (in this case, 8000) is already being used by another process. The API fails to bind to the port, and therefore, it cannot start.

### How to Resolve

1. **Find the Process Using the Port:**

   Open your terminal and run:
   
   ````shell
   lsof -i :8000

   The error indicates that port 8000 is in use. To free it up, open your terminal and run:

   lsof -i :8000


   This will list the process ID (PID) using the port. Then kill the process with:

   kill -9 <PID>

   http://localhost:8001/responses

Get a random response:
http://localhost:8001/responses/random

You can also add query parameters to filter, for example:

http://localhost:8001/responses?limit=5&output_text=overthinking

