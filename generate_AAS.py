#parse through the tex
#find figures
#replace filename with .eps
#create/cleanup target directory
#convert list of files
#copy other necessary files
import re,os

#target = 'arxiv_submission'
project=os.path.basename(os.getcwd())
target = 'apj_submission_1'

if target.startswith('arxiv'):
    tex = open('ms-arxiv.tex').read()
    plots = re.findall('\\includegraphics.*\{([^}]+)\}',tex)
else:
    tex = open('ms.tex').read()
#    plots = re.findall('\{figures\/(\S*)\}',tex)
    plots = re.findall('\\includegraphics.*\]{(.*)\}',tex)

#clean out the '}'s from the figure paths
l = ['a','b','c','d']
eps_plots = [None]*len(plots)
print len(eps_plots)
plot_filenames = [None]*len(plots)
for i in xrange(len(plots)):
    print plots[i]
    plot_filenames[i] = plots[i].replace('}','').replace('{','')
    if i in [0,1,2,3]:
        eps_plots[i] = 'f{n}.eps'.format(n=i+1)
    if i>3:
        eps_plots[i] = 'f5{letter}.eps'.format(letter=l[i-4])


try:
    os.mkdir(target)
except(OSError):
    os.system('rm -rf %s'%target)
    os.mkdir(target)
#eps_plots = [p[:-4]+'.eps' for p in plots]
#Copy the plots to the new directory and point at the new figures in the tex
for i,plot in enumerate(plots):
    print plot,plot_filenames[i],'->',eps_plots[i]
    if target.startswith('arxiv'):
        print "cp ",plot_filenames[i],target
        os.system('cp %s %s/'%(plot_filenames[i],target))
        tex = tex.replace(plot,plot)
        print plot
    else:
        print "cp ",plot_filenames[i],target
        os.system('convert %s %s/%s'%(plot_filenames[i],target,eps_plots[i]))
        print 'convert %s %s/%s'%(plot_filenames[i],target,eps_plots[i])
        print 'inserting ',eps_plots[i].replace('.eps','')
        tex = tex.replace(plot,eps_plots[i].replace('.eps',''))

#replace bibliography 
#\bibliography{library}
bib = open('ms.bbl').read()
tex = tex.replace('\\bibliography{library,aliu}',bib)
out = open('%s/ms.tex'%target,'w')
out.write(tex)
#os.system('cp figures/tab1.txt figures/tab2.txt %s'%target)
if target.startswith('arxiv'):
    os.system('tar -cjf %s.tar.bz2 %s/*'%(target,target))
else:
    os.system('tar -czf {project}_{target}.tar.bz2 {target}/*'.format(target=target,project=project))



