#!/usr/bin/python
# coding: UTF-8
import sys
from datetime import datetime as dt
import json
import re
import copy
import random
import math
import datetime
import ConfigParser

class DataClass:
	def __init__(self):
		self.__file = ""
		self.__data = ""

	def show(self):
		print json.dumps(self.__data, indent = 4)
	
	def set_data(self, data):
		self.__data = data

	def get_data(self):
		return self.__data
	
	def get_nodes(self):
		return self.__data["nodes"]

	def get_nodes_count(self):
		return len(self.__data["nodes"])
		
	def get_node_id(self, i):
		return self.__data["nodes"][i]["id"]

	def get_node_size(self, i):
		return self.__data["nodes"][i]["size"]
	
	def get_node_size_with_id(self, id):
		return self.get_node_size(self.get_node_index_with_id(id))
		
	def get_node_label(self, i):
		return self.__data["nodes"][i]["label"]
	
	def get_node_label_with_id(self, id):
		return self.get_node_label(self.get_node_index_with_id(id))

	def get_node_id_with_label(self, label):
		id = "none"
		for i in range(len(self.__data["nodes"])):
			if label.find(self.__data["nodes"][i]["label"]) == 0:
				# hit
				id = self.__data["nodes"][i]["id"]

		return id
	
	def get_node_index_with_id(self, id):
		index = -1
		for i in range(len(self.__data["nodes"])):
			if self.__data["nodes"][i]["id"] == id:
				index = i
		return index
	
	def set_node_x(self, i, x):
		self.__data["nodes"][i]["x"] = x
		pass

	def set_node_y(self, i, y):
		self.__data["nodes"][i]["y"] = y
		pass

	def set_node_color(self, i, color):
		pass

	def set_node_label(self, i, label):
		pass
	
	def set_node_size(self, i, size):
		self.__data["nodes"][i]["size"] = size

	def set_node_size_with_id(self, id, size):
		self.set_node_size(self.get_node_index_with_id(id), size)

	def set_node_id(self, i, id):
		self.__data["nodes"][i]["id"] = id
		
	def set_node_update_date(self, i, day):
		self.__data["nodes"][i]["update"] = day
		
	def set_node_update_date_with_id(self, id, day):
		self.set_node_update_date(self.get_node_index_with_id(id), day)
		
	def create_new_node(self, color, label, y, x, id, size, day):
		self.__data["nodes"].append({"color":color, "label":label, "y":y, "x":x, "id":id, "size":size, "entry":day, "update":day})
		
	def create_new_edge(self, color, source, id, target, day):
		self.__data["edges"].append({"color":color, "source":source, "id":id, "target":target, "entry":day, "update":day})

	def get_edge_id_with_source_target(self, source, target):
		id = "none"
		for i in range(len(self.__data["edges"])):
			if self.__data["edges"][i]["source"] == source:
				if self.__data["edges"][i]["target"] == target:
					# hit
					id = self.__data["edges"][i]["id"]
		return id
		
	def get_edge_index_with_id(self, id):
		index = -1
		for i in range(len(self.__data["edges"])):
			if self.__data["edges"][i]["id"] == id:
				index = i
		return index

	def get_edges_count(self):
		return len(self.__data["edges"])

	def get_edge_source(self, i):
		return self.__data["edges"][i]["source"]

	def get_edge_source_with_id(self, id):
		return self.get_edge_source(self.get_edge_index_with_id(id))
	
	def get_edge_target(self, i):
		return self.__data["edges"][i]["target"]

	def get_edge_target_with_id(self, id):
		return self.get_edge_target(self.get_edge_index_with_id(id))
		
	def get_edge_id(self, i):
		return self.__data["edges"][i]["id"]

	def set_edge_id(self, i, id):
		self.__data["edges"][i]["id"] = id
	
	def set_edge_source(self, i, source):
		self.__data["edges"][i]["source"] = source
	
	def set_edge_source_with_id(self, id, source):
		self.set_edge_source(self.get_edge_index_with_id(id), source)

	def set_edge_target(self, i, target):
		self.__data["edges"][i]["target"] = target
	
	def set_edge_target_with_id(self, id, target):
		self.set_edge_target(self.get_edge_index_with_id(id), target)
		
	def set_edge_update_date(self, i, day):
		self.__data["edges"][i]["update"] = day
		
	def set_edge_update_date_with_id(self, id, day):
		self.set_edge_update_date(self.get_edge_index_with_id(id), day)
		
	def del_edge(self, i):
		self.__data["edges"].pop(i)

	def del_edge_with_id(self, id):
		self.del_edge(self.get_edge_index_with_id(id))


class JsonDataClass(DataClass):
	def __init__(self, file):
		DataClass.__init__(self)
		f = open(file, "r")
		DataClass.set_data(self, json.load(f))
		f.close()
		
	def reset(self):
		DataClass.set_data(self, {"nodes": [],"edges": []})

		
class M3u8DataClass(DataClass):
	def __init__(self):
		DataClass.__init__(self)
		DataClass.set_data(self, {"nodes":[], "edges":[]})
		self.__new_node_ids = []
		self.__old_node_ids = []
		self.__new_edge_ids = []
		self.__old_edge_ids = []
		self.__labels = []
		
	def load_m3u8(self, file):
		print "loading",file, "..."
		f = open(file, "r")
		#self.__data = {"nodes":[], "edges":[]}
		for line in f:
			if re.match("#EXTINF",line):
				label = re.sub("#EXTINF(.[0-9]{3,4}[,])","",line).strip()
				self.__labels.append(label)
				print "    import ", label
		f.close()

		print "finish loading!"
		
	def get_m3u8_label(self, i):
		return self.__labels[i]
		
	def get_m3u8_labels_count(self):
		return len(self.__labels)

	def append_new_node_id(self, id):
		self.__new_node_ids.append(id)

	def get_new_node_id(self, i):
		return self.__new_node_ids[i]

	def get_new_node_ids_count(self):
		return len(self.__new_node_ids)

	def append_old_node_id(self, id):
		self.__old_node_ids.append(id)

	def get_old_node_id(self, i):
		return self.__old_node_ids[i]

	def get_old_node_ids_count(self):
		return len(self.__old_node_ids)

	def append_new_edge_id(self, id):
		self.__new_edge_ids.append(id)

	def get_new_edge_id(self, i):
		return self.__new_edge_ids[i]

	def get_new_edge_ids_count(self):
		return len(self.__new_edge_ids)

	def append_old_edge_id(self, id):
		self.__old_edge_ids.append(id)

	def get_old_edge_id(self, i):
		return self.__old_edge_ids[i]

	def get_old_edge_ids_count(self):
		return len(self.__old_edge_ids)

def mixplaylist(pl1, pl2, outpl):
	list_pl1 = []
	list_pl2 = []
	list_outpl = []
	f = open(pl1,"r")
	i = 0
	for line in f:
		# first line EXT1M3U skipped
		if i != 0:
			list_pl1.append(line)
		elif i == 0:
			header = line
		i += 1
	f.close()

	f = open(pl2,"r")
	i = 0
	for line in f:
		# first line EXTM3U skipped
		if i != 0:
			list_pl2.append(line)
		i += 1
	f.close()

	# import pdb; pdb.set_trace()
	idx_a = 0
	idx_b = 0
	while idx_a < len(list_pl1):
		if idx_a != len(list_pl1):
			list_outpl.append(list_pl1[idx_a])
			idx_a += 1
		if idx_a != len(list_pl1):
			list_outpl.append(list_pl1[idx_a])
			idx_a += 1
		if idx_b != len(list_pl2):
			list_outpl.append(list_pl2[idx_b])
			idx_b += 1
		if idx_b != len(list_pl2):
			list_outpl.append(list_pl2[idx_b])
			idx_b += 1

	list_outpl.insert(0, header)

	# tdatetime = dt.now()
	# tstr = tdatetime.strftime('%Y-%m-%d')
	# file3 = "MIXED HISTORY_"+tstr+".m3u8"
	file3 = outpl
	f = open(file3, "w")
	for line in list_outpl:
		f.write(line)
	f.close()

	print ""
	print "finish mixing!!"
	print "the mixed playlist file is",file3
	print ""


if __name__ == "__main__":

	inifile = ConfigParser.SafeConfigParser()
	inifile.read("./config.ini")
	# data = JsonDataClass("data.json")
	data = JsonDataClass(inifile.get("settings","file"))

	while 1:
		print "type command..."
		input_line = raw_input()
		if input_line == "exit":
			break
		elif input_line == "mixpl":
			print ""
			print "mix 2 playlist mutually..."
			print "input fist playlist"
			pl1 = raw_input()
			print "input second playlist"
			pl2 = raw_input()
			print "out playlist"
			outpl = raw_input()
			mixplaylist(pl1, pl2, outpl)
		elif input_line == "load":
			# sequence diagram
			# https://creately.com/diagram/isi7szk61/ZdBFzRm5MscjkiipVY4ee11xM%3D
			print "load m3u8 format playlist."
			print "select m3u8 file..."
			input_file = raw_input()
			#input_file = "test.m3u8"
			m3u8 = M3u8DataClass()
			m3u8.load_m3u8(input_file)
			for i in range(m3u8.get_m3u8_labels_count()):
				print m3u8.get_m3u8_label(i)
				m3u8.create_new_node("rgb(255,204,102)", m3u8.get_m3u8_label(i), 0, 0, "", 1, "")

			# update node id for m3u8 data
			new_node_id_number = data.get_nodes_count()
			for i in range(m3u8.get_nodes_count()):
				id = data.get_node_id_with_label(m3u8.get_node_label(i))
				if id == "none":
					m3u8.set_node_id(i, "n"+str(new_node_id_number))
					m3u8.append_new_node_id(m3u8.get_node_id(i))
					new_node_id_number += 1
				else:
					m3u8.set_node_id(i, id)
					m3u8.append_old_node_id(m3u8.get_node_id(i))

			# create edge for m3u8 data
			for i in range(m3u8.get_nodes_count()-1):
				source = m3u8.get_node_id(i)
				target = m3u8.get_node_id(i + 1)
				m3u8.create_new_edge("rgb(128, 128, 128)", source, "", target, "")

			# update edge id for m3u8
			new_edge_id_number = data.get_edges_count()
			for i in range(m3u8.get_edges_count()):
				id = data.get_edge_id_with_source_target(m3u8.get_edge_source(i), m3u8.get_edge_target(i))
				if id == "none":
					m3u8.set_edge_id(i, "e"+str(new_edge_id_number))
					m3u8.append_new_edge_id(m3u8.get_edge_id(i))
					new_edge_id_number += 1
				else:
					m3u8.set_edge_id(i, id)
					m3u8.append_old_edge_id(m3u8.get_edge_id(i))

			m3u8.show()
		elif input_line == "set":
			#import pdb; pdb.set_trace()
			print "set m3u8 to data"
			print "new node count", m3u8.get_new_node_ids_count()
			for i in range(m3u8.get_new_node_ids_count()):
				print "new node id", m3u8.get_new_node_id(i)
				posx = random.uniform(-1,1)
				posy = random.uniform(-1,1)
				size = 1
				id = m3u8.get_new_node_id(i)
				label = m3u8.get_node_label_with_id(id)
				color = "rgb("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+")"
				today = datetime.date.today().isoformat()
				data.create_new_node(color, label, posy, posx, id, size, today)

			for i in range(m3u8.get_old_node_ids_count()):
				print "old node id", m3u8.get_old_node_id(i)
				data.set_node_size_with_id(m3u8.get_old_node_id(i), data.get_node_size_with_id(m3u8.get_old_node_id(i)) + 1)
				data.set_node_update_date_with_id(m3u8.get_old_node_id(i), datetime.date.today().isoformat())

			for i in range(m3u8.get_new_edge_ids_count()):
				color = "rgb(128, 128, 128)"
				today = datetime.date.today().isoformat()
				data.create_new_edge(color, m3u8.get_edge_source(i), m3u8.get_new_edge_id(i), m3u8.get_edge_target(i), today)

			for i in range(m3u8.get_old_edge_ids_count()):
				data.set_edge_update_date_with_id(m3u8.get_old_node_id(i), datetime.date.today().isoformat())

			data.show()
		elif input_line == "commit":
			f = open ("data.json", "w")
			json.dump(data.get_data(), f)
			f.close()
			print "commit data.json"
			break
		elif input_line == "del":
			print "type edges index"
			id = raw_input()
			data.del_edge_with_id(id)
			data.show()
		elif input_line == "reset":
			data.reset()
		elif input_line == "show":
			data.show()
			print datetime.date.today().isoformat()
		else:
			print "again"






