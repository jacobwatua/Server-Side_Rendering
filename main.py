#FUNCTION open file in write mode
import os
class ScaffoldProject:
    def __init__(self, path, projectTitle) -> None:
        self.pathName = path
        self.projectName = projectTitle
        self.scaffoldProject()
    
    def scaffoldProject(self):
        #navigate to project path
        os.chdir(self.pathName)
        #create project folder
        print("Scafolding project, Please wait...")
        os.mkdir(self.projectName)
        os.chdir(self.projectName)
        self.write_file('package.json', '')
        self.writePackages()
        #os.system('npm i')
        #create folders  "utilities, views, routes, public"
        self.createFolder('utilities')
        self.createFolder('views')
        self.createFolder('routes')
        self.createFolder('public')
        self.createFolder('public/images')
        self.createFolder('public/js')
        self.createFolder('public/css')
        self.createIndexJs()
        self.createRoutes()
        self.createFileReader()
        self.createContentTypeReader()
        self.createIndexHtml()
        self.createPrettierConfig()
        #print scaffold message
        print("Project scaffold successfully")
        print("Installing packages")
        os.system('npm i')
        print("Installation complete")
        print("Formating Js code")
        os.system("npm run format")
        self.createTailwindConfig()
        self.createPostCss()
        self.createStylesCss()
        os.system("npm run build")
        self.createGitignore()
        print("Format complete")
        print("- cd {}".format(self.projectName))
        print("- npm run start to start the server")


    #function to create folders
    def createFolder(self, folderName):
        os.mkdir(folderName)


    def writePackages(self):
        self.write_file('package.json', '''
    {\n
    "name": "serve_html",
    "version": "1.0.0",
    "description": "",
    "main": "index.js",
    "scripts": {
      "start": "node index.js",
      "format": "prettier --write .",
      "build": "postcss public/css/styles.css -o public/css/build/styles.css",
      "watch:css": "postcss public/css/styles.css -o public/css/build/styles.css --watch",
      "test": "echo \\\"Error: no test specified\\\" && exit 1"
    },
    "keywords": [],
    "author": "",
    "license": "ISC",
    "dependencies": {},
    "devDependencies": {
        "autoprefixer": "^10.4.16",
        "http": "^0.0.1-security",
        "http-status-codes": "^2.3.0",
        "postcss": "^8.4.31",
        "tailwindcss": "^3.3.5",
        "@tailwindcss/forms": "^0.5.7",
        "prettier": "^3.1.0"
    }
    }\n''')

    def write_file(self, filename, text):
        with open(filename, 'w') as f:
            return f.write(text)
    def createIndexJs(self):
        #create index.js contnent
        indexJs = """
        const routes = require("./routes/router");
        const { ReadContentType } = require("./utilities/contentTypeReader");
        const port = 3000,
        http = require("http"),
        httpStatus = require("http-status-codes");

        http
        .createServer((req, res) => {
            let url = req.url;
            if (routes[req.method][url]) {
            routes[req.method][url](req, res);
            } else {
            ReadContentType(url, res);
            }
        })
        .listen(port);
        """
        self.write_file('index.js', indexJs)

    def createRoutes(self):
        routes = """
        // ./routes/router.js
        const httpStatus = require("http-status-codes");
        const routes = {
            GET: {
                    "/sample": (req, res) => {
                    // Handle GET /sample
                    res.writeHead(httpStatus.StatusCodes.OK, {
                        "Content-Type": "application/json",
                    });
                    res.end(JSON.stringify({ status: "Recieved" }));
                    },
            },
            POST: {
                "/sample": (req, res) => {
                // Handle POST /sample
                res.writeHead(httpStatus.StatusCodes.OK, {
                    "Content-Type": "text/plain",
                });
                res.end("Sample POST route");
                },
            },
        };
        module.exports = routes;\n"""
        self.write_file('routes/router.js', routes)

    #Function to create fileReader utility
    def createFileReader(self):
        fileReader = """
        const fs = require("fs"),
        httpStatus = require("http-status-codes");
        const sendErrorResponse = (res) => {
        res.writeHead(httpStatus.StatusCodes.NOT_FOUND, {
            "Content-Type": "text/html",
        });
        res.write("<h1>File Not Found!</h1>");
        res.end();
        };

        const customReader = (file_path, res) => {
        if (fs.existsSync(file_path)) {
            fs.readFile(file_path, (error, data) => {
            if (error) {
                console.log(error);
                sendErrorResponse(res);
                return;
            }
            res.write(data);
            res.end();
            });
        } else {
            sendErrorResponse(res);
        }
        };
        module.exports = {
        customReader,
        sendErrorResponse,
        };
        """
        self.write_file('utilities/fileReader.js', fileReader)

    def createContentTypeReader(self):
        contentReader = """
        const httpStatus = require("http-status-codes");
        const { sendErrorResponse, customReader } = require("../utilities/fileReader");

        /**
        * ReadContentType - Checks the file type being requested, updates HEADERS,
        * and writes data using fs
        * @param {*} url - file path based on 'req.url'
        * @param {*} res - response object
        *
        * @returns - No return value
        */
        function ReadContentType(url, res) {
        if (url.indexOf(".html") !== -1) {
            res.writeHead(httpStatus.StatusCodes.OK, {
            "Content-Type": "text/html",
            });
            customReader(`./views${url}`, res);
        } else if (url == "/") {
            res.writeHead(httpStatus.StatusCodes.OK, {
            "Content-Type": "text/html",
            });
            customReader(`./views${url}/index.html`, res);
        } else if (url.indexOf(".js") !== -1) {
            res.writeHead(httpStatus.StatusCodes.OK, {
            "Content-Type": "text/javascript",
            });
            customReader(`./public/js${url}`, res);
        } else if (url.indexOf(".css") !== -1) {
            res.writeHead(httpStatus.StatusCodes.OK, {
            "Content-Type": "text/css",
            });
            customReader(`./public/css${url}`, res);
        } else if (url.indexOf(".png") !== -1) {
            res.writeHead(httpStatus.StatusCodes.OK, {
            "Content-Type": "image/png",
            });
            customReader(`./public/images${url}`, res);
        } else if (url.indexOf(".jpg") !== -1 || url.indexOf(".jpeg") !== -1) {
            res.writeHead(httpStatus.StatusCodes.OK, {
            "Content-Type": "image/jpeg",
            });
            customReader(`./public/images${url}`, res);
        } else {
            sendErrorResponse(res);
        }
        }

        module.exports = {
        ReadContentType,
        };

        """
        self.write_file('utilities/contentTypeReader.js', contentReader)
    #function to create index.html
    def createIndexHtml(self):
        indexHtml = """
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link rel="stylesheet" href="/build/styles.css" />
                <title>Simple Server</title>
            </head>
            <body class="bg-gray-900 text-white h-[100vh] text-sm">
                <div class="h-full flex flex-col items-center justify-center">
                    <h1>Server side rendering</h1>
                    <div class="my-2 mx-auto flex gap-3 items-center justify-center">
                        <a
                            class="bg-black text-white py-2 px-3 rounded hover:bg-gray-900 hover:border-white hover:border-2"
                            href="https://www.educative.io/answers/what-is-server-side-rendering"
                        >
                            Learn More
                        </a>
                        <a
                            class="bg-transparent border border-white border-spacing-2 text-white py-2 px-3 rounded hover:bg-white hover:text-black"
                            href = "https://github.com/jacobwatua/Server-Side_Rendering"
                        >
                            Contribute
                        </a>
                    </div>
                </div>
            </body>
        </html>

        """
        self.write_file('views/index.html', indexHtml)
    def createPrettierConfig(self):
        prettier_config = """
        {
            "singleQuote": true,
            "semi": false,
            "useTabs": true,
            "tabWidth": 4
        }
        """
        self.write_file('.prettierrc', prettier_config)
    #function to create postcss.config.js
    def createPostCss(self):
        #create postcss.config.js
        postcss = """
        module.exports = {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
        }
        """
        self.write_file("postcss.config.js", postcss)
    #function to overwrite tailwind.config.js
    def createTailwindConfig(self):
        tailwind_config = """
       /** @type {import('tailwindcss').Config} */
        module.exports = {
        content: ["./views/**/*.{html,js}"],
        darkMode: "class",
        theme: {
            extend: {
            colors: {
                darkOlive: "#09090b",
            },
            fontFamily: {
                lato: [
                "Josefin Sans, sans-serif",
                "Jost, sans-serif",
                "Lato, sans-serif",
                "Merriweather, serif",
                "Poppins, sans-serif",
                ],
            },
            },
        },
        plugins: [require("@tailwindcss/forms")],
        };
        """
        self.write_file("tailwind.config.js", tailwind_config)
    #FUNCTION to create styles.css
    def createStylesCss(self):
        stylesCss = """
        @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&family=Jost&family=Lato&family=Merriweather:wght@300;400&family=Nunito:wght@500&family=Poppins&display=swap');
        @import 'tailwindcss/base';
        @import 'tailwindcss/components';
        @import 'tailwindcss/utilities';
        body {
            font-family: 'Josefin Sans', sans-serif;
            font-family: 'Jost', sans-serif;
            font-family: 'Lato', sans-serif;
            font-family: 'Merriweather', serif;
            font-family: 'Nunito', sans-serif;
            font-family: 'Poppins', sans-serif;
        }
        """
        self.write_file("public/css/styles.css", stylesCss)
    #FUNCTION to create .gitignore
    def createGitignore(self):
        gitignore = """
        node_modules
        package-lock.json
        .env
        build
        public/css/build
        .vscode
        """
        self.write_file(".gitignore", gitignore)
projectName = input("Enter Project Name: ")

try:
    assert projectName, "Project name cannot be empty"
    scaffoldProject = ScaffoldProject('.//', projectName)
except AssertionError as a:
    print(a)


