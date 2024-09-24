FROM mageai/mageai:llm

ARG PROJECT_NAME=zoomcamp-smart-mail
ARG MAGE_CODE_PATH=/zoomcamp-smart-mail/mage
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}
ARG MAGE_DATA_DIR=${MAGE_CODE_PATH}/mage_data


# Set the MAGE_CODE_PATH variable to the path of the Mage code.
ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}"

WORKDIR ${MAGE_CODE_PATH}

# Replace [project_name] with the name of your project (e.g. demo_project)
COPY ${PROJECT_NAME} ${PROJECT_NAME}

# Set the USER_CODE_PATH variable to the path of user project.
# The project path needs to contain project name.
# Replace [project_name] with the name of your project (e.g. demo_project)
ENV USER_CODE_PATH=${USER_CODE_PATH}

# Set the MAGE_DATA_DIR variable to the path of the Mage data directory.
ENV MAGE_DATA_DIR=${MAGE_DATA_DIR}

# Set the number of versions
ENV MAX_NUMBER_OF_FILE_VERSIONS=2

RUN pip install --upgrade pip

# Install nltk
RUN pip install nltk

# Install custom Python libraries if requirements.txt exists
RUN if [ -f ${USER_CODE_PATH}/requirements.txt ]; then pip3 install -r ${USER_CODE_PATH}/requirements.txt; fi
# Install custom libraries within 3rd party libraries (e.g. DBT packages) if install_other_dependencies.py exists
RUN if [ -f /app/install_other_dependencies.py ]; then python3 /app/install_other_dependencies.py --path ${USER_CODE_PATH}; fi


CMD ["/bin/sh", "-c", "/app/run_app.sh"]
