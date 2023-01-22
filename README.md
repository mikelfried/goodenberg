# goodenberg
Convert documents with a simple REST api.

It uses **libreoffice** headless convert, and **unoserver**, which is the newer unoconv.

Including support for:
* `doc`, `docx`
* `xls`, `xlsx`
* `ppt`, `pptx`

to `pdf`

# Deploy with docker
```
docker pull 21pilots/goodenberg[:TAG]
docker run -p [YOUR PORT]:80 21pilots/goodenberg[:TAG]
```

# Open API Docs
```
connect to `localhost:[YOUR PORT]/docs`
```

# Benchmarks

Faster than gotenberg and onlyoffice. 
Has support for RTL languages unlike onlyoffice.
