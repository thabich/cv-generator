# Project Details

## Pretext
This project is an experiment. I used ChatGPT to design a system that allows me to structure my CV in a searchable format.  
It runs only in a local Docker container, with no exposure to external sources. Since it is intended for personal use (or for anyone curious enough to try it), minor errors are acceptable given the experimental nature.

## Goal of the Project
The final result of this project can be seen on my [homepage](https://www.findichgut.net).  
This component provides a WebUI to generate JSON files that store:

- Job titles (to ensure consistent naming conventions)  
- Skills (in English, and in German if they differ)  
- Certifications, linked to relevant skills  
- Projects with task lists, where each task is again linked to skills  

The goal is to enable filtering by skills and to provide extracts of certifications and project tasks related to those skills.  
Additionally, it will be possible to generate a complete list of certifications and a full résumé.

## How to Run
Clone this repository and start the container with:
```bash
docker compose up

## Takeaways
The takeaways from this experiment are published on my [blog post](https://www.findichgut.net).
