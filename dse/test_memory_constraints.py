def str_to_bool(v):
    # Convert "true" to True and "false" to False
    v = str(v)
    return v.lower() in ("true", "t", "1", "yes", "y")

class MemoryEstimator:
    def __init__(self, symbol_map_value): 
        self.num_npus = symbol_map_value["num_npus"]
        self.dp = symbol_map_value["dp"]
        self.pp = symbol_map_value["pp"]
        self.sp = symbol_map_value["sp"]
        self.mp = self.num_npus // (self.dp*self.pp*self.sp)
        self.din = symbol_map_value["din"]
        self.dout = symbol_map_value["dout"]
        self.dff = symbol_map_value["dff"]
        self.dmodel = symbol_map_value["dmodel"]
        self.batch = symbol_map_value["batch"]
        if not 'seq' in symbol_map_value:
            if 'prefilling' in symbol_map_value:
                self.seq = symbol_map_value["prefilling"]
            elif 'decoding' in symbol_map_value:
                self.seq = symbol_map_value["decoding"]
            else:
                assert False
        else:
            self.seq = symbol_map_value["seq"]
        self.head = symbol_map_value["head"]
        self.num_stacks = symbol_map_value["num_stacks"]
        self.weight_sharded = str_to_bool(symbol_map_value["weight_sharded"])
        
    def mha_weights(self):
        if self.weight_sharded:
            return 3*self.dmodel*self.dmodel/self.mp
        else:
            return 3*self.dmodel*self.dmodel/(self.mp*self.dp*self.sp)
    
    def emb_weight(self):
        return self.dmodel*(self.din+self.dout)/self.mp
    
    def ffn_weights(self):
        return self.dmodel*self.dff*2/self.mp
    
    def mha_activation(self):
        q = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        k = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        v = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        qk = self.batch*self.seq*self.seq*self.head/(self.dp*self.mp*self.sp)
        qkv = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        add = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        norm = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        return q+k+v+qk+qkv+add+norm
    
    def ffn_activation(self):
        x1 = self.batch*self.seq*self.dff/(self.dp*self.mp*self.sp)
        x2 = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        add = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        norm = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
        return x1+x2+add+norm
    
    def emb_activation(self):
        if self.weight_sharded:
            in_emb = self.batch*self.seq*self.dmodel/(self.dp*self.mp*self.sp)
            out_emb = self.batch*self.seq*self.dout/(self.dp*self.mp*self.sp)
        else:
            in_emb = self.batch*self.seq*self.dmodel/(self.dp*self.sp)
            out_emb = self.batch*self.seq*self.dout/(self.dp*self.sp)
        return in_emb+out_emb
    
    def total_memory(self):
        return (self.mha_weights() + self.emb_weight() + self.ffn_weights() + self.mha_activation() + self.ffn_activation() + self.emb_activation())*2*self.num_stacks/self.pp

    @classmethod
    def get_total_memory(cls, symbol_map_value):
        return cls(symbol_map_value).total_memory()
    
if __name__ == '__main__':
    num_npus = 1024
    dp = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    pp = [1, 2, 4]
    sp = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    symbol_map_value = {
        "num_npus": 1024,
        "dp": 1,
        "pp": 1,
        "sp": 128,
        "weight_sharded": 0,
        "din": 12288,
        "dout": 12288,
        "dff": 49152,
        "dmodel": 12288,
        "batch": 2048,
        "seq": 2048,
        "head": 96,
        "num_stacks": 4
    }

    for ddp in dp:
        for ppp in pp:
            for ssp in sp:
                mmp = num_npus / (ddp*ppp*ssp)
                if mmp < 1:
                    continue
                symbol_map_value["dp"] = ddp
                symbol_map_value["pp"] = ppp
                symbol_map_value["sp"] = ssp
                print("dp: {}, pp: {}, sp: {}, total memory: {}".format(ddp, ppp, ssp, MemoryEstimator.get_total_memory(symbol_map_value)))
