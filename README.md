# prsconv3
Convert Tombo files to CSV

## Roadmap
- [x] Start with prscovn2.py. Update its CLI in a way that makes sense for a tool that will accept multiple kinds of file input, not just `.tombo.per_read_stats` files. Make the user specify long or wide-format output for `.tombo.per_read_stats` files.
- [ ] Add browser-file-->CSV converters (wiggle and bedgraph).
- [ ] Add direct `.tombo.stats`-->CSV converter
- [ ] Get test coverage as high as I can
- [ ] Package and upload to PyPI
- [ ] Set up some kind of CI tool
- [ ] Get lots of fast5 files for tests. Add fast5-->CSV converter. (Assume all fast5s look like the ones I have.)
