// socket.cpp: 定義應用程式的進入點。
//

#include "socket.h"

using namespace std;

class nmessage {
public:
	virtual string formal() { return msg; }
	nmessage(string i) :msg(i) {}
	nmessage() {}
private:
	string msg;

};

class Delete : public nmessage {
private:
	vector <string>content;
public:
	Delete() {
		string sentance;
		getline(cin, sentance);

		while (sentance[0] != '#')
		{
			content.push_back(sentance);
			getline(cin, sentance);
		}
	}
	string formal() {
		string ret;
		for (auto s : content) {
			ret.append(s);
			ret.append("\n");
		}
		return ret;
	}
};

class Quit : public nmessage {
public:
	Quit() {};
	string formal() {
		return "QUIT";
	}
};

class Get : public nmessage {
public:
	Get() {};
	string formal() {
		return "GET";
	}

};

class Post : public nmessage {
private:
	vector <string>content;
public:
	Post() {
		string sentance;
		getline(cin, sentance);

		while (sentance[0] != '#')
		{
			content.push_back(sentance);
			getline(cin, sentance);
		}
	}
	string formal() {
		string ret;
		for (auto s : content) {
			ret.append(s);
			ret.append("\n");
		}
		return ret;
	}

};

class socket
{
public:
	socket(string ip, auto port);
	~socket();
	void start() { tcp_client.open(); }
	void addcommand(string m);
	void sendAndreceive();
	void block();
private:
	nmessage* packet;
	MinimalSocket::Port server_port;
	MinimalSocket::tcp::TcpClient<true> tcp_client;
	string address;

};

socket::socket(string ip, auto port):address(ip),server_port(port),tcp_client(MinimalSocket::Address{ ip,port }),packet(nullptr){}

socket::~socket() { tcp_client.shutDown(); }

void socket::addcommand(const string m)
{
	if (m == "POST")
		packet = new Post;
	else if (m == "GET")
		packet = new Get();
	else if (m == "DELETE")
		packet = new Delete();
	else if (m == "QUIT")
		packet = new Quit();
	else packet = new nmessage(m);

}

void socket::sendAndreceive()
{
	string rcvbuf;
	//check method, if string is needed, send METHOD to server to initiate it first
	if (typeid(Post) == typeid(*packet))
		tcp_client.send("POST");
	else if (typeid(Delete) == typeid(*packet))
		tcp_client.send("DELETE");

	// Tie string from multiple line into one
	stringstream buf(packet->formal());

	string send;
	while (buf >> send)
	{
		tcp_client.send(send);
		// As sending the packets so rapidly will lead to packet unflavourable concatination from server, time is need to for server to clear buffer
		this_thread::sleep_for(chrono::milliseconds(300));
	}

	


	if (typeid(Post) == typeid(*packet) || typeid(Delete) == typeid(*packet))
	{
		tcp_client.send("#");
		this_thread::sleep_for(chrono::milliseconds(300));
	}
	

	rcvbuf = tcp_client.receive(4096);
	
	if(typeid(Get) ==  typeid(*packet))
		while (rcvbuf.back() != '#') {
			cout << rcvbuf << endl;
			this_thread::sleep_for(chrono::milliseconds(300));
			rcvbuf = tcp_client.receive(4096);
		}

	cout << rcvbuf << endl;


	if (typeid(Quit) == typeid(*packet) && rcvbuf == "OK") {
		cout << "Quit gracefully." << endl;
		tcp_client.shutDown();
		exit(0);
	}

	delete packet;
	packet = nullptr;
}







int main()
{
	
	socket c_socket("127.0.0.1", MinimalSocket::Port(16111));
	c_socket.start();
	string command;
	while (cin >> command) {
		c_socket.addcommand(command);
		c_socket.sendAndreceive();
	}
	return 0;
}
