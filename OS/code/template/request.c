#include "io_helper.h"
#include "request.h"
#include <pthread.h>
#include <string.h>

#define MAXBUF (8192)

//
//	TODO: add code to create and manage the buffer
//

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;  // for the entering and editing the buffers
pthread_cond_t condEmpty = PTHREAD_COND_INITIALIZER; // for sending signal that buffer is no more empty
pthread_cond_t condFull = PTHREAD_COND_INITIALIZER; // for sending signal that buffer is no more full

typedef struct mybuffer{
    int fd;
    char filename[MAXBUF];      // structure for elements of buffer
    int filesize;
} myBuffer;

typedef struct queue {
    int front;
    int rear;                   // wrapper struct for queue (circular) buffer for FIFO
    myBuffer* reqQ;
} Queue;

Queue* buff_q = NULL;         // buff_q = buffer queue (circular)
int initQ = 0;                // boolean to check whether the queue buffer is initialized or not

typedef struct minheap {
    int heapSize;
    myBuffer* reqT;             // wrapper struct for min heap buffer for SFF
} minHeap;

minHeap* buff_t = NULL;       // buff_t = buffer tree
int initT = 0;                // boolean to check whether the min heap buffer is initialized or not

int isBuffFull() {
    if(!scheduling_algo) {
        if((buff_q->front == buff_q->rear + 1) || (buff_q->front == 0 && buff_q->rear == buffer_max_size - 1))
            return 1;
        return 0;             // check whether the buffer struct being used is full or not
    } else {
        if(buff_t->heapSize == buffer_max_size)
            return 1;
        return 0;
    }
}

int isBuffEmpty() {
    if(!scheduling_algo) {
        if(buff_q->front == -1) return 1;
        return 0;                              // check whether the buffer struct being used is empty or not
    } else {
        if(buff_t->heapSize <= 0)
            return 1;
        return 0;
    }
}

void initBuffQ() {
    buff_q = malloc(sizeof(Queue));
    buff_q->front = -1;                        // initialize buffer queue for FIFO
    buff_q->rear = -1;
    buff_q->reqQ = malloc(sizeof(myBuffer)*buffer_max_size);
}

void putToBuffQ(int fd, char filename[], int filesize) {
    if(buff_q->front == -1) 
        buff_q->front = 0;
    buff_q->rear = (buff_q->rear + 1) % buffer_max_size;    // Add element into buffer queue

    buff_q->reqQ[buff_q->rear].fd = fd;
    strcpy(buff_q->reqQ[buff_q->rear].filename, filename);
    buff_q->reqQ[buff_q->rear].filesize = filesize;

    pthread_cond_broadcast(&condEmpty);         // wake all threads waiting for taking an element from buffer
}

myBuffer* getFromBuffQ() {
    if(isBuffEmpty()) {
        printf("Buffer Empty!\n");
        return NULL;
    }

    myBuffer* retval = malloc(sizeof(myBuffer));

    retval->fd = buff_q->reqQ[buff_q->front].fd; 
    strcpy(retval->filename, buff_q->reqQ[buff_q->front].filename);
    retval->filesize = buff_q->reqQ[buff_q->front].filesize; 

    if(buff_q->front == buff_q->rear)           // Remove an element from the buffer and return it
        buff_q->front = buff_q->rear = -1;
    else 
        buff_q->front = (buff_q->front + 1) % buffer_max_size;

    pthread_cond_broadcast(&condFull);         // wake all threads waiting for inserting an element into the buffer

    return retval;
}

int getParent(int index) { return (index - 1)/2; }
int getLeftChild(int index) { return 2*index + 1; } // to get index of Left child of node at index i 
int getRightChild(int index) { return 2*index + 2; } // to get index of Right child of node at index i

void swap(int index1, int index2) {
    int tempFd,tempFilesize;            // swap elements of buffer at indices index1 and index2
    char tempFilename[MAXBUF];

    tempFd = buff_t->reqT[index1].fd;
    buff_t->reqT[index1].fd = buff_t->reqT[index2].fd;
    buff_t->reqT[index2].fd = tempFd;

    strcpy(tempFilename, buff_t->reqT[index1].filename);
    strcpy(buff_t->reqT[index1].filename, buff_t->reqT[index2].filename);
    strcpy(buff_t->reqT[index1].filename, tempFilename);

    tempFilesize = buff_t->reqT[index1].filesize;
    buff_t->reqT[index1].filesize = buff_t->reqT[index2].filesize;
    buff_t->reqT[index2].filesize = tempFilesize;
}

void initBuffT() {
    buff_t = malloc(sizeof(minHeap));         // initialize buffer tree for SFF
    buff_t->heapSize = 0;
    buff_t->reqT = malloc(sizeof(myBuffer)*buffer_max_size);
}

void putToBuffT(int fd, char filename[], int filesize) {
    int i = buff_t->heapSize;

    buff_t->reqT[i].fd = fd;
    strcpy(buff_t->reqT[i].filename, filename);      // Insert the new element at the end of buffer
    buff_t->reqT[i].filesize = filesize;
    buff_t->heapSize += 1;

    while (i != 0 && buff_t->reqT[getParent(i)].filesize > buff_t->reqT[i].filesize) { 
        swap(i, getParent(i)); 
        i = getParent(i);            // check if min heap property still holds if not fix it
    } 

    pthread_cond_broadcast(&condEmpty);   // wake all threads waiting for taking an element from buffer
}
 
void minHeapify(int index) { 
    int l,r,smallest;

    l = getLeftChild(index);        // Recursive method to heapify the tree with the root at given index
    r = getRightChild(index); 
    smallest = index; 

    if (l < buff_t->heapSize && buff_t->reqT[l].filesize < buff_t->reqT[index].filesize) 
        smallest = l; 
    if (r < buff_t->heapSize && buff_t->reqT[r].filesize < buff_t->reqT[smallest].filesize) 
        smallest = r; 
    if (smallest != index) { 
        swap(index, smallest); 
        minHeapify(smallest);      // recursive call to heapify the subtree with root at smallest
    } 
} 

myBuffer* getFromBuffT() { 
    if(isBuffEmpty()) {
        printf("Buffer Empty!\n");
        return NULL; 
    }

    myBuffer* retval = malloc(sizeof(myBuffer));

    retval->fd = buff_t->reqT[0].fd;
    strcpy(retval->filename, buff_t->reqT[0].filename);   
    retval->filesize = buff_t->reqT[0].filesize;

    if(buff_t->heapSize == 1) {        // Remove an element from the buffer tree and return it 
        buff_t->heapSize -= 1;
        return retval;
    } 
    
    swap(0, buff_t->heapSize - 1); 
    buff_t->heapSize -= 1;
    minHeapify(0);                     // heapify to make the buffer obey min heap property again

    pthread_cond_broadcast(&condFull); // wake all threads waiting for inserting an element into the buffer 
  
    return retval; 
} 

//
// Sends out HTTP response in case of errors
//
void request_error(int fd, char *cause, char *errnum, char *shortmsg, char *longmsg)
{
  char buf[MAXBUF], body[MAXBUF];

  // Create the body of error message first (have to know its length for header)
  sprintf(body, ""
                "<!doctype html>\r\n"
                "<head>\r\n"
                "  <title>OSTEP WebServer Error</title>\r\n"
                "</head>\r\n"
                "<body>\r\n"
                "  <h2>%s: %s</h2>\r\n"
                "  <p>%s: %s</p>\r\n"
                "</body>\r\n"
                "</html>\r\n",
          errnum, shortmsg, longmsg, cause);

  // Write out the header information for this response
  sprintf(buf, "HTTP/1.0 %s %s\r\n", errnum, shortmsg);
  write_or_die(fd, buf, strlen(buf));

  sprintf(buf, "Content-Type: text/html\r\n");
  write_or_die(fd, buf, strlen(buf));

  sprintf(buf, "Content-Length: %lu\r\n\r\n", strlen(body));
  write_or_die(fd, buf, strlen(buf));

  // Write out the body last
  write_or_die(fd, body, strlen(body));

  // close the socket connection
  close_or_die(fd);
}

//
// Reads and discards everything up to an empty text line
//
void request_read_headers(int fd)
{
  char buf[MAXBUF];

  readline_or_die(fd, buf, MAXBUF);
  while (strcmp(buf, "\r\n"))
  {
    readline_or_die(fd, buf, MAXBUF);
  }
  return;
}

//
// Return 1 if static, 0 if dynamic content (executable file)
// Calculates filename (and cgiargs, for dynamic) from uri
//
int request_parse_uri(char *uri, char *filename, char *cgiargs)
{
  char *ptr;

  if (!strstr(uri, "cgi"))
  {
    // static
    strcpy(cgiargs, "");
    sprintf(filename, ".%s", uri);
    if (uri[strlen(uri) - 1] == '/')
    {
      strcat(filename, "index.html");
    }
    return 1;
  }
  else
  {
    // dynamic
    ptr = index(uri, '?');
    if (ptr)
    {
      strcpy(cgiargs, ptr + 1);
      *ptr = '\0';
    }
    else
    {
      strcpy(cgiargs, "");
    }
    sprintf(filename, ".%s", uri);
    return 0;
  }
}

//
// Fills in the filetype given the filename
//
void request_get_filetype(char *filename, char *filetype)
{
  if (strstr(filename, ".html"))
    strcpy(filetype, "text/html");
  else if (strstr(filename, ".gif"))
    strcpy(filetype, "image/gif");
  else if (strstr(filename, ".jpg"))
    strcpy(filetype, "image/jpeg");
  else
    strcpy(filetype, "text/plain");
}

//
// Handles requests for static content
//
void request_serve_static(int fd, char *filename, int filesize)
{
  int srcfd;
  char *srcp, filetype[MAXBUF], buf[MAXBUF];

  request_get_filetype(filename, filetype);
  srcfd = open_or_die(filename, O_RDONLY, 0);

  // Rather than call read() to read the file into memory,
  // which would require that we allocate a buffer, we memory-map the file
  srcp = mmap_or_die(0, filesize, PROT_READ, MAP_PRIVATE, srcfd, 0);
  close_or_die(srcfd);

  // put together response
  sprintf(buf, ""
               "HTTP/1.0 200 OK\r\n"
               "Server: OSTEP WebServer\r\n"
               "Content-Length: %d\r\n"
               "Content-Type: %s\r\n\r\n",
          filesize, filetype);

  write_or_die(fd, buf, strlen(buf));

  //  Writes out to the client socket the memory-mapped file
  write_or_die(fd, srcp, filesize);
  munmap_or_die(srcp, filesize);
}

//
// Fetches the requests from the buffer and handles them (thread locic)
//
void *thread_request_serve_static(void *arg)
{
  // TODO: write code to actualy respond to HTTP requests

  while(1) {                         // infinite loop to keep the thread from dying after finishing one request
    if(!scheduling_algo) {                     // for FIFO requests
        pthread_mutex_lock(&lock);             // acquire lock to enter buffer through any func

        while(buff_q == NULL || isBuffEmpty()) 
            pthread_cond_wait(&condEmpty, &lock);   // release lock and wait for not empty signal from putToBuffQ() 

        myBuffer* req = getFromBuffQ();
        
        request_serve_static(req->fd,req->filename,req->filesize);
        close_or_die(req->fd);                      // close connection between this client and server
        printf("Request for %s is removed from the buffer.\n", req->filename);
        
        pthread_mutex_unlock(&lock);        // release lock to allow other threads to enter the buffer
    } 
    else {                                  // for SFF requests
        pthread_mutex_lock(&lock);            // acquire lock to enter buffer through any func

        while(buff_t == NULL || isBuffEmpty()) 
            pthread_cond_wait(&condEmpty, &lock);      // release lock and wait for not empty signal from putToBuffT() 

        myBuffer* req = getFromBuffT();
        
        request_serve_static(req->fd,req->filename,req->filesize);
        close_or_die(req->fd);                      // close connection between this client and server
        printf("Request for %s is removed from the buffer.\n", req->filename);
        pthread_mutex_unlock(&lock);         // release lock to allow other threads to enter the buffer
    } 
  }
}

//
// Initial handling of the request
//
void request_handle(int fd)
{
  int is_static;
  struct stat sbuf;
  char buf[MAXBUF], method[MAXBUF], uri[MAXBUF], version[MAXBUF];
  char filename[MAXBUF], cgiargs[MAXBUF];

  // get the request type, file path and HTTP version
  readline_or_die(fd, buf, MAXBUF);
  sscanf(buf, "%s %s %s", method, uri, version);
  printf("method:%s uri:%s version:%s\n", method, uri, version);

  // verify if the request type is GET is not
  if (strcasecmp(method, "GET"))
  {
    request_error(fd, method, "501", "Not Implemented", "server does not implement this method");
    return;
  }
  request_read_headers(fd);

  // check requested content type (static/dynamic)
  is_static = request_parse_uri(uri, filename, cgiargs);

  if(strstr(filename,"..")) {
    request_error(fd, filename, "404", "Forbidden", "Traversing up in filesystem is not allowed");
    return;
  }

  // get some data regarding the requested file, also check if requested file is present on server
  if (stat(filename, &sbuf) < 0)
  {
    request_error(fd, filename, "404", "Not found", "server could not find this file");
    return;
  }

  // verify if requested content is static
  if (is_static)
  {
    if (!(S_ISREG(sbuf.st_mode)) || !(S_IRUSR & sbuf.st_mode))
    {
      request_error(fd, filename, "403", "Forbidden", "server could not read this file");
      return;
    }

    // TODO: write code to add HTTP requests in the buffer based on the scheduling policy
    if(!scheduling_algo) {         // for FIFO requests
        if(!initQ) {
            initBuffQ();           
            initQ = 1;             // set to 1 to indicate queue is already initialized
        }
        
        pthread_mutex_lock(&lock);    // acquire lock to enter buffer through any func
        while(isBuffFull())
            pthread_cond_wait(&condFull,&lock);     // release lock and wait for not full signal from getFromBuffQ() 
        
        putToBuffQ(fd, filename, sbuf.st_size);  // Add element into buffer queue
      
        pthread_mutex_unlock(&lock);    // release lock to allow other threads to enter the buffer
    } else {                     // for SFF requests
        if(!initT) {
            initBuffT();
            initT = 1;           // set to 1 to indicate tree is already initialized
        }
        
        pthread_mutex_lock(&lock);   // acquire lock to enter buffer through any func
        while(isBuffFull())
            pthread_cond_wait(&condFull,&lock);      // release lock and wait for not full signal from getFromBuffT() 
        
        putToBuffT(fd, filename, sbuf.st_size);  // Add element into buffer tree
      
        pthread_mutex_unlock(&lock);   // release lock to allow other threads to enter the buffer  
    }
    
    printf("Request for %s is added to the buffer.\n", filename);
  }
  else
  {
    request_error(fd, filename, "501", "Not Implemented", "server does not serve dynamic content request");
  }
}
