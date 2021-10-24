#Include Iterator.ahk
equals(obj, other) {
	if(IsObject(obj) && !isObject(other) || !IsObject(obj) && isObject(other))
		return false
	if !isObject(obj) {
		return obj == other
	}
	if(isObject(obj.Equals)) {
		return obj.Equals(other)
	}
	it := new ZippedIterator(obj, other)
	while(it.hasNext()) {
		values := it.next()
		if(!equals(values[1], values[2]) || !equals(values[3], values[4])){
			return false
		}
	}
	return true
}
