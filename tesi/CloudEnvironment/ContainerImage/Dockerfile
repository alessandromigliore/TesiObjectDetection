FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY main.py ${LAMBDA_TASK_ROOT}

COPY model_loader.py ${LAMBDA_TASK_ROOT}

RUN mkdir model

COPY deploy_model_algo_1-symbol.json ${LAMBDA_TASK_ROOT}/model

COPY deploy_model_algo_1-0000.params ${LAMBDA_TASK_ROOT}/model

COPY hyperparams.json ${LAMBDA_TASK_ROOT}/model

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN yum -y install tar gzip zlib freetype-devel \
    gcc \
    ghostscript \
    lcms2-devel \
    libffi-devel \
    libimagequant-devel \
    libjpeg-devel \
    libraqm-devel \
    libtiff-devel \
    libwebp-devel \
    make \
    openjpeg2-devel \
    rh-python36 \
    rh-python36-python-virtualenv \
    sudo \
    tcl-devel \
    tk-devel \
    tkinter \
    which \
    xorg-x11-server-Xvfb \
    zlib-devel \
    && yum clean all

RUN yum -y install libgomp

RUN yum -y install libquadmath

RUN yum -y install mesa-libGL

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.lambda_handler" ]
