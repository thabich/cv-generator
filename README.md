# Project details
## Pretext
This project, is an experiment. I used ChatGPT to create a project, which allows me to structure my CV in a searchable format.
I think this project is qualified as there is no exposure of the project to external sources. It's only spun up on a local docker container.
As it is only used by me (or if you're brave enough by you), some errors can be accepted.

## Goal of this project
The final result of this project can be seen on my [homepage](https://www.findichgut.net).
This part is providing a WebUI to generate JSON files storing:

- job titles (to have unique naming conventions)
- skills (in English and if it differs German)
- certifications, which are linked to skills
- projects with a list of tasks in those projects, each task is linked again to skills

Goal of the project is to allow to filter by skills and to provide an extract of my certifications and project tasks which are related to those skils.
Further more it will be possible to create a full list of certifications and a full resumee.

## How to run this
Just clone this repository and run
```bash
docker compose up
```
## Take aways
The take aways of this experient are published on my [website](www.findichgut.net)
