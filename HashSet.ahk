#Include HashSetNode.ahk
#Include Equals.ahk
#Include Hasher.ahk

class HashSet {
	__New() {
		this.table := []
		this.capacity := 1
		this.size := 0
	}
	add(key)	{
		index := Mod(hash(key), this.capacity)
		newNode := new HashSetNode(key)
		if(!this.table[index]) {
			this.table[index] := newNode
		} else {
			current := this.table[index]
			previous := ""
			while(current) {
				if(equals(current.getKey(), key)) {
					current.setValue(value)
					return
				}
				previous := current
				current := current.getNext()
			}
			previous.setNext(newNode)
			this.size++
		}
	}
	contains(key) {
		index := Mod(hash(key), this.capacity)
		if(!this.table[index]) {
			return false
		}
		node := this.table[index]
		previous := ""
		while(node) {
			if(equals(node.getKey(), key)){
				return True
			}
			node := node.getNext()
		}
		return false
	}
	remove(key) {
		index := Mod(hash(key), this.capacity)
		node := this.table[index]
		previous := ""
		while(node) {
			if(equals(node.getKey(), key)){
				if(!previous)
					this.table[index] := node.getNext()
				else {
					previous.setNext(node.getNext())
				}
				return
			}
			node := node.getNext()
		}
	}
	get(key) {
		index := Mod(hash(key), this.capacity)
		if(!this.table[index]) {
			return false
		}
		node := this.table[index]
		previous := ""
		while(node) {
			if(equals(node.getKey(), key)){
				return node.getKey()
			}
			node := node.getNext()
		}
		return ""
	}
	union(other) {
		table2 := new HashSet()
		for key, val in this.table
			table2.add(key)
		for key, val in other.table
			table2.add(key)
		return table2
	}
	class Enumerator {
        __New(HashSet) {
            local
            this._BucketsEnum  := HashSet.table._NewEnum()
           ,this._PreviousItem := ""
            return this
        }
		
		Next(byref Key) {
            local
            if (this._PreviousItem == "" or this._PreviousItem.Next == "") {
                Result := this._BucketsEnum.Next(_, Item)
            } else {
                Item   := this._PreviousItem.Next, Result := true
            }
            if (Result) {
                Key := Item.Key, this._PreviousItem := Item
            }
            return Result
        }
    }
	
    _NewEnum() {
        local
        global HashSet
		array := []
		for key, val in this.table {
			current := val
			while(current) {
				array.push(current.getKey())
				current := current.getNext()
			}
			this.array := array
		}
        return new HashSet.Enumerator(this)
    }
	iter() {
		return new HashSet.Iterator(this)
	}
	size() {
		return this.size
	}
	class Iterator {
		__New(set) {
			this.array := []
			for item in set {
				this.array.push(item)
			}
			this.i := 1
		}
		Next(){
			return this.array[this.i++]
		}
		HasNext() {
			return this.i <= this.array.Count()
		}
	}
	
	Equals(other) {
		if(other.__Class != this.__Class) {
			return false
		}
		it1 := this.iter()
		it2 := other.iter()
		while(it1.HasNext() && it2.HasNext()) {
			if(!equals(it1.Next(), it2.Next()))
				return False
		}
		if(it1.HasNext() || it2.HasNext())
			return False
		return True
	}
}
 
findSet(sets, target) {
	for i, set in sets
		for j, val in set
			if(val = target)
				return i
}
