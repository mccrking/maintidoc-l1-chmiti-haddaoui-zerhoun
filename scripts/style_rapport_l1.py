from reportlab.lib import colors

def appliquer_style(namespace):
    for key in ('NAVY','TEAL','INK','GRAY'):namespace[key]=colors.black
    namespace['PALE']=colors.white
    for style in namespace['ST'].values():style.textColor=colors.black
    original=namespace['table']
    if not getattr(original,'_noir',False):
        def table_noire(*args,**kwargs):
            t=original(*args,**kwargs)
            t._bkgrndcmds=[]
            t._linecmds=[]
            from reportlab.platypus import TableStyle
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('GRID',(0,0),(-1,-1),.45,colors.black)]))
            return t
        table_noire._noir=True
        namespace['table']=table_noire

def table_pour_rapport(T):
    def render(*args,**kwargs):
        t=T(*args,**kwargs)
        t._bkgrndcmds=[];t._linecmds=[]
        from reportlab.platypus import TableStyle
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('GRID',(0,0),(-1,-1),.45,colors.black)]))
        return t
    return render
