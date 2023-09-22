Docker setup for those who want to test server functionality locally.
This is not required to solve the challenge, and probably won't work on the haaukins vm.

Run the following commands.
docker build -t psygame .
docker run -d --name psygame psygame