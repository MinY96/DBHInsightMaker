using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DBHTab.Models
{
    public class ChartNode
    {
        public string Header { get; set; }
        public string GroupTag { get; set; }
        public string TypeTag { get; set; }
        public ObservableCollection<ChartNode> Children { get; set; } = new ObservableCollection<ChartNode>();
        public bool IsLeaf => Children == null || Children.Count == 0;
    }
}
