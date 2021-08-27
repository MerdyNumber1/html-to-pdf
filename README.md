# Simple API for converting HTML to PDF file
  
## How to start:  
Copy and fill `.env.example` to `.env`

### Production:
`docker-compose --file docker-compose.prod.yml up --build`
### Development
`docker-compose --file docker-compose.dev.yml up --build`

## API schema for converting:
POST-request on `http(s)://host:$APP_PORT/` with body:  
`{  
  "html": ["<div>page 1</div>", "<div>page 2</div>"]  
}`  

where html property is an array, where items are pages of future PDF-document.
