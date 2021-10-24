class HashSetNode {
    __New(key :="") {
        this.key := key
        this.next := ""
    }

    getKey() {
        return this.key
    }

    getNext() {
        return this.next
    }

    setKey(key) {
        this.key := key
    }

    setNext(next) {
        this.next := next
    }
	
	hasNext() {
		return this.next != ""
    }
}