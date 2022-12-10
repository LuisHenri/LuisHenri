import datetime as dt
import logging
import os
from github import Github

# Get environment variables
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]

# Extract repository name because it's combined with username
repositoryName = GITHUB_REPOSITORY.split("/")[1]


def main():
    logging.info("Starting aging script...")
    birthday = dt.date(1999, 9, 24)
    today = dt.date.today()

    # Calculate age and cast to str
    age = str(
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )

    file_path = "README.md"

    g = Github(ACCESS_TOKEN)
    repo = g.get_user().get_repo(repositoryName)

    file = repo.get_contents(file_path)
    content = file.decoded_content.decode()

    if age not in content:
        template_file_path = ".github/scripts/aging/README_template.md"
        template_file = repo.get_contents(template_file_path)
        template_content = template_file.decoded_content.decode()

        new_content = template_content.replace("{{ AGE }}", age)
        repo.update_file(file_path, "feat: happy bday to me! 🎉", new_content, file.sha)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        logging.info("Caught keyboard interrupt")
    except Exception as err:
        logging.error(err, exc_info=True)
    finally:
        logging.info("Exiting...")
