# Choose the base image
FROM raspberrypi-7514dd1cfcaa49ceb338ea1d935db8bb-base

# Create the user
RUN groupadd --gid ${template:HOST_USER_GID} ${template:HOST_USER_NAME} \
    && useradd --uid ${template:HOST_USER_UID} --gid ${template:HOST_USER_GID} -m ${template:HOST_USER_NAME} \
    # Add sudo support
    && apt-get update && apt-get install -y sudo acl \
    && echo ${template:HOST_USER_NAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${template:HOST_USER_NAME} \
    && chmod 0440 /etc/sudoers.d/${template:HOST_USER_NAME}

# Set the default user
USER ${template:HOST_USER_NAME}