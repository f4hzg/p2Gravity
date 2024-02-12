#coding: utf8
import p2api

class Template(dict):
    def __init__(self, *args, **kwargs):
        super(Template, self).__init__(*args, **kwargs)
        self.ob_id = None
        self.version = -1        
        self.template_id = None
        self.template_Name = None
        self.template_type = None        
        return None

    def populate_from_yml(self, yml):
        """
        A method to populate existing fields from yml dict
        Note that no new field is created
        """
        for key in yml:
            if key in self.params:
                self[key] = yml[key]
        return None
    
    def __getattribute__(self, name):
        if name == "params":
            return self._params()
        return object.__getattribute__(self, name)    

    def _params(self):
        return dict(self)
            
    def p2_create(self, api, ob_id):
        tpl, version = api.createTemplate(ob_id, self.template_name)
        self.ob_id = ob_id        
        self.version = version
        self.tpl = tpl
        return None
        
    def p2_update(self, api):
        # at update, check that the number of values in OFFSETS is the same as in sequence
        if "SEQ.RELOFF.X" in self:
            nobj = len(self["SEQ.OBSSEQ"].split())
            # add 0s to match length
            self["SEQ.RELOFF.X"] = self["SEQ.RELOFF.X"]+[0]*(nobj-len(self["SEQ.RELOFF.X"]))
            self["SEQ.RELOFF.Y"] = self["SEQ.RELOFF.Y"]+[0]*(nobj-len(self["SEQ.RELOFF.X"]))
        tpl, version = api.setTemplateParams(self.ob_id, self.tpl, self.params, self.version)
        self.version = version
        self.tpl = tpl
        return None
        
