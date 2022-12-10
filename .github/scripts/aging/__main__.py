import datetime as dt
import logging
import os
import re
from github import Github

# Get environment variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Extract repository name because it's combined with username
repository_name = GITHUB_REPOSITORY.split("/")[1]
readme_path = "README.md"


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

    g = Github(ACCESS_TOKEN)
    repo = g.get_user().get_repo(repository_name)

    file = repo.get_contents(readme_path)
    content = file.decoded_content.decode()

    age_section_regex = rf"<!--START_SECTION:aging-->(\d*)<!--END_SECTION:aging-->"
    age_section_regex_pat = re.compile(age_section_regex, re.MULTILINE)

    if age != age_section_regex_pat.search(content).group(1):
        logging.info("Updating age...")
        content = re.sub(
            age_section_regex_pat, age_section_regex.replace(r"(\d*)", age), content
        )
        repo.update_file(readme_path, "feat: happy bday to me! 🎉", content, file.sha)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        logging.info("Caught keyboard interrupt")
    except Exception as err:
        logging.error(err, exc_info=True)
    finally:
        logging.info("Exiting...")
